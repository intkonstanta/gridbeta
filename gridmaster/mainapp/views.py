
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import DetailView
from django.template import Library
from django.utils import timezone
from django.core.files import File
from json import loads, dumps
from .models import *
from .forms import *
import logging
import random
import json
from pathlib import Path
import os



from string import ascii_letters, digits
import turtle


DIGITS = digits
LETTERS = ascii_letters
CALLS = ["right", "left", "up", "down", "call"]
KEYWORDS = ["endrepeat", "endif", "endproc", "repeat", "ifblock", "procedure", "set", "else"]

"""
Грамматика языка (в форме EBNF)
===============================

Program = Procedures Body;
Procedures = { Procedure };
Procedure = "procedure" word Program "endproc";
Body = ( IfBlock | Expr | LoopBlock ) { Body };
IfBlock = "ifblock" "dir" Body { "else" Body } "endif";
LoopBlock = "repeat" Arg Body "endrepeat";
Expr = SetExpr | FuncCall | MathExpr;
SetExpr = "set" word "=" MathExpr;
FuncCall = "keyword" Arg;
MathExpr = MathTerm { "+" MathTerm | "-" MathTerm };
MathTerm = MathFactor { "*" MathFactor | "//" MathFactor };
MathFactor = MathPower { "^" MathPower };
MathPower = Arg | "(" MathExpr ")" | "-" MathPower;
Arg = word | number;
number = "0".."9" { number };
word = ("a".."z" | "A".."Z" | "_") { word };
"""

###############
# TOKENS
###############

class Error(Exception):
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result
    
    def __repr__(self):
        return self.as_string()

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

class ParseError(Error):
    def __init__(self, pos, message):
        super().__init__('Parse Error', (pos, message))


TT_INT      = 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_POW      = 'POW'
TT_SET      = 'SET'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_WORD     = 'WORD'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

    def __str__(self):
        return self.__repr__()

###############
# LEXER
###############
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t\n':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS, "+"))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS, "-"))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, "*"))
                self.advance()
            elif self.current_char == "//":
                tokens.append(Token(TT_DIV, "//"))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == "=":
                tokens.append(Token(TT_SET))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(TT_POW, "^"))
                self.advance()
            elif self.current_char in LETTERS + '_':
                tokens.append(self.make_word())
            else:
                char = self.current_char
                self.advance()
                raise IllegalCharError("'" + char + "'")

        return tokens
    
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == ".":
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

    def make_word(self):
        word_str = ''

        while self.current_char not in {None} and self.current_char in LETTERS + '_':
            word_str += self.current_char
            self.advance()

        return Token(TT_WORD, word_str)


###############
# PARSER
###############
    
class Parser:
    def __init__(self, program):
        self.pos = 0
        self.program = program

    def error(self, message):
        raise ParseError(self.pos, message)

    def peek(self) -> Token:
        if self.pos < len(self.program):
            return self.program[self.pos]
        return Token(None)

    def next(self) -> Token:
        token = self.peek()
        self.pos += 1
        return token

    def check_Arg(self, token: Token):
        return token.type in {TT_WORD, TT_INT} and token.value not in KEYWORDS + CALLS

    def check_MathExpr(self, token: Token):
        return token.type in {TT_LPAREN, TT_MINUS} or self.check_Arg(token)

    def check_SetExpr(self, token: Token):
        return token.type == TT_WORD and token.value == "set"

    def check_FuncCall(self, token: Token):
        return token.type == TT_WORD and token.value in CALLS

    def check_Expr(self, token):
        return self.check_MathExpr(token) or \
               self.check_FuncCall(token) or \
               self.check_SetExpr(token)

    # axiom = Program;
    def parse(self):
        result = self.parse_Program()
        if self.peek().type != None:
            self.error(f"Expected EOF, got: {self.peek()}")
        return result

    # Program = Procedures Body;
    def parse_Program(self):
        procedures = self.parse_Procedures()
        body = self.parse_Body()

        result = {}
        if procedures != []:
            result['procedures'] = procedures
        if body != []:
            result['body'] = body

        return result

    # Procedures = { Procedure };
    def parse_Procedures(self):
        result = []
        while self.peek().value == "procedure":
            result += [self.parse_Procedure()]
        return result

    # Procedure = "procedure" word Program "endproc";
    def parse_Procedure(self):
        if self.next().value != "procedure":
            self.error("procedure")

        name = self.next()
        if name.type != TT_WORD:
            self.error("word")

        program = self.parse_Program()

        if self.next().value != "endproc":
            self.error("endproc")

        return {name.value: program}

    # Body = ( IfBlock | Expr | LoopBlock ) { Body };
    def parse_Body(self):
        result = []
        while self.peek().value in {"ifblock", "repeat"} or self.check_Expr(self.peek()):
            if self.peek().value == "ifblock":
                result += [self.parse_IfBlock()]
            elif self.peek().value == "repeat":
                result += [self.parse_LoopBlock()]
            else:
                result += [self.parse_Expr()]

        return result

    # LoopBlock = "repeat" Arg Body "endrepeat";
    def parse_LoopBlock(self):
        if self.next().value != "repeat":
            self.error("repeat")

        times = self.next()
        if times.type not in (TT_INT, TT_WORD):
            self.error("number")

        body = self.parse_Body()
        if self.next().value != "endrepeat":
            self.error("endrepeat")

        return ['repeat', times, body]

    # IfBlock = "ifblock" "dir" Body { "else" Body } "endif";
    def parse_IfBlock(self):
        if self.next().value != "ifblock":
            self.error("ifblock")

        result = {}
        dir = self.next()
        if dir.value not in {'right', 'left', 'up', 'down'}:
            self.error("dir")

        result[dir] = self.parse_Body()
        if self.peek().value == "else":
            self.next()
            result['else'] = self.parse_Body()
        else:
            result['else'] = []

        if self.next().value != "endif":
            self.error("endif")

        return ['if', result]

    # Expr = SetExpr | FuncCall | MathExpr;
    def parse_Expr(self):
        if not self.check_Expr(self.peek()):
            self.error("peek")

        if self.check_SetExpr(self.peek()):
            return self.parse_SetExpr()

        if self.check_FuncCall(self.peek()):
            return self.parse_FuncCall()

        return self.parse_MathExpr()

    # FuncCall = "keyword" Arg;
    def parse_FuncCall(self):
        keyword = self.next()
        if keyword.type != TT_WORD and keyword in KEYWORDS:
            self.error("keyword")
        return [keyword.value, self.parse_Arg().value]

    # SetExpr = "set" word "=" MathExpr;
    def parse_SetExpr(self):
        if self.next().value != "set":
            self.error("set")

        word = self.next()
        if word.type != TT_WORD:
            self.error("word")

        if self.next().type != TT_SET:
            self.error("=")

        result = self.parse_MathExpr()

        if len(result) == 1:
            result = result[0]

        return ['set', word.value, result]

    # MathExpr = MathTerm { "+" MathTerm | "-" MathTerm };
    def parse_MathExpr(self):
        result = self.parse_MathTerm()

        while self.peek().type in (TT_PLUS, TT_MINUS):
            op = self.next()
            term = self.parse_MathTerm()
            result += [op]
            if len(term) == 1:
                result += term
            else:
                result += [term]

        return result

    # MathTerm = MathFactor { "*" MathFactor | "/" MathFactor };
    def parse_MathTerm(self):
        result = self.parse_MathFactor()

        while self.peek().type in (TT_MUL, TT_DIV):
            op = self.next()
            term = self.parse_MathFactor()
            result += [op]
            if len(term) == 1:
                result += term
            else:
                result += [term]

        return result

    # MathFactor = MathPower { "^" MathPower };
    def parse_MathFactor(self):
        result = self.parse_MathPower()

        while self.peek().type == TT_POW:
            op = self.next()
            term = self.parse_MathFactor()
            result += [op]
            if len(term) == 1:
                result += term
            else:
                result += [term]

        return result

    # MathPower = Arg | "(" MathExpr ")" | "-" MathPower;
    def parse_MathPower(self):
        if self.peek().type == TT_LPAREN:
            self.next()
            result = self.parse_MathExpr()
            if self.next().type != TT_RPAREN:
                self.error(")")
        elif self.peek().type == TT_MINUS:
            result = [self.next(), self.parse_MathPower()]
        else:
            result = [self.parse_Arg().value]

        return result

    # Arg = word | number;
    def parse_Arg(self):
        result = self.next()
        if not self.check_Arg(result):
            self.error("result")
        return result











####################
# HANDLER
####################



class Handler:

    def __init__(self, data):
        self.data = data
        self.current_x = 0
        self.current_y = 0
        self.main_body = []
        self.vars_obj_list = {}
        self.json_data = {"0": [0, 0], }
        self.current_action = 0

        print(self.data)

    def ifblock(self, dir):
        if dir == "right":
            return self.current_x == 20
        elif dir == "left":
            return self.current_x == 0
        elif dir == "up":
            return self.current_y == 20
        elif dir == "down":
            return self.current_y == 0
        else:
            print("Unknown dir") 
    
    def get_current_cors(self):
                return (self.current_x, self.current_y)
    
    def recur_iter(self, obj):
        if type(obj) == list:
            print(f"Get list: {obj}")
            if "set" in obj:
                print("set")
                print(obj)
                if type(self.recur_iter(obj[2])) not in {float, int, list}:
                    print(f"Error - incorrect type of the assigned value. A variable of type {type(obj[2])} has been introduced, but can only be int and float")
                    self.json_data["Error"] = [f"Error - incorrect type of the assigned value. A variable of type {type(obj[2])} has been introduced, but can only be int and float"]
                print(type(self.recur_iter(obj[2])))
                print(self.recur_iter(obj[2]))
                self.vars_obj_list[obj[1]] = self.recur_iter(obj[2])

            elif "repeat" in obj:
                print("repeat")
                body = obj[2]
                count = self.recur_iter(obj[1])
                c = 0
                if count < 1 or count > 1000:
                    print(f"Error - incorrect parameter in repeat, equals {count}. The parameter must be in the range from 1 to 1000.")
                    self.json_data["Error"] = [f"Error - incorrect parameter in repeat, equals {count}. The parameter must be in the range from 1 to 1000."]
                else:
                    for i in range(count):
                        c += 1
                        print(c)
                        self.recur_iter([body])

            elif "if" in obj:
                dir_str = list(obj[1].keys())[0].value
                if self.ifblock(dir_str):
                    self.recur_iter(obj[1][list(obj[1].keys())[0]])
                else:
                    self.recur_iter(obj[1]['else'])


            elif "call" in obj:
                print("Call")
                print(obj)
                if obj[1] not in self.vars_obj_list:
                    print(f"Error - undefined procedure, name {obj[1]}")
                    self.json_data["Error"] = [f"Error - undefined procedure, name {obj[1]}"]
                else:
                    print(self.vars_obj_list[obj[1]])
                    self.recur_iter(self.vars_obj_list[obj[1]])

            elif "right" in obj:
                print(f"Move right - {obj}")
                self.current_action += 1
                self.current_x += self.recur_iter(obj[1])
            
                print(self.get_current_cors())
                self.json_data[self.current_action] = [self.current_x, self.current_y]
                if self.recur_iter(obj[1]) < 1 or self.recur_iter(obj[1]) > 1000:
                    print(f"Error - Executor has left the field, cords: {self.get_current_cors()}")
                    self.json_data["Error"] = [f"Incorrect parametr in move obj {obj[0]}: {self.get_current_cors()}"]
                if self.current_x < 0 or self.current_x > 20:
                    print(f"Error - Executor has left the field, cords: {self.get_current_cors()}")
                    self.json_data["Error"] = [f"Error - Executor has left the field, cords: {self.get_current_cors()}"]
                    
                return []

            elif "left" in obj:
                print(f"Move left - {obj}")
                self.current_action += 1
                self.current_x -= self.recur_iter(obj[1])
              
                print(self.get_current_cors())
                self.json_data[self.current_action] = [self.current_x, self.current_y]
                if self.recur_iter(obj[1]) < 1 or self.recur_iter(obj[1]) > 1000:
                    print(f"Error - Executor has left the field, cords: {self.get_current_cors()}")
                    self.json_data["Error"] = [f"Incorrect parametr in move obj {obj[0]}: {self.get_current_cors()}"]
                
                if self.current_x < 0 or self.current_x > 20:
                    
                    print(f"Error - Executor has left the field, cords: {self.get_current_cors()}")
                    self.json_data["Error"] = [f"Error - Executor has left the field, cords: {self.get_current_cors()}"]
                
                    
                return []

            elif "up" in obj:
                print(f"Move up - {obj}")
                self.current_action += 1
                self.current_y += self.recur_iter(obj[1])
          
                print(self.get_current_cors())
                self.json_data[self.current_action] = [self.current_x, self.current_y]
                if self.recur_iter(obj[1]) < 1 or self.recur_iter(obj[1]) > 1000:
                    print(f"Error - Executor has left the field, cords: {self.get_current_cors()}")
                    self.json_data["Error"] = [f"Incorrect parametr in move obj {obj[0]}: {self.get_current_cors()}"]
              
                if self.current_y < 0 or self.current_y > 20:
                    print(f"Error - Executor has left the field, cords: {self.get_current_cors()}")
                    self.json_data["Error"] = [f"Error - Executor has left the field, cords: {self.get_current_cors()}"]
                    
                return []

            elif "down" in obj:
                print(f"Move down - {obj}")
                self.current_action += 1
                self.current_y -= self.recur_iter(obj[1])
       
                print(self.get_current_cors())
                self.json_data[self.current_action] = [self.current_x, self.current_y]
                if self.recur_iter(obj[1]) < 1 or self.recur_iter(obj[1]) > 1000:
                    print(f"Error - Executor has left the field, cords: {self.get_current_cors()}")
                    self.json_data["Error"] = [f"Incorrect parametr in move obj {obj[0]}: {self.get_current_cors()}"]
                
                if self.current_y < 0 or self.current_y > 20:
                    print(f"Error - Executor has left the field, cords: {self.get_current_cors()}")
                    self.json_data["Error"] = [f"Error - Executor has left the field, cords: {self.get_current_cors()}"]
                
                return []
            
            elif Token in obj:
                print("Token")
                n = len(obj)
                for indx in range(n):
                    if obj[indx] == Token:
                        signs = {
                            "PLUS": "+",
                            "MINUS": "-",
                            "POW": "^",
                            "DIV": "//",
                            "MUL": "*",
                        }

                        if obj[indx].value == None:
                            obj[indx] = signs[obj[indx].type]
                        else:
                            obj[indx] = obj[indx].value

                print(obj)
                

            elif "+" in obj:
                print(f"Error - unknown string symbol - {obj}")
                print(1/0)


            elif "-" in obj:
                print(f"Error - unknown string symbol - {obj}")
                print(1/0)
            
            elif "//" in obj:
                print(f"Error - unknown string symbol - {obj}")
                print(1/0)
            
            elif "*" in obj:
                print(f"Error - unknown string symbol - {obj}")
                print(1/0)

            elif "^" in obj:
                print(f"Error - unknown string symbol - {obj}")
                print(1/0)


            else:
                if any([type(i) == Token for i in obj]):
                    print("Expr token")
                    for i in range(len(obj)):
                        x = obj[i]
                        if type(x) == Token:
                            obj[i] = self.recur_iter(obj[i])
                    self.recur_iter(obj)
                else:
                    print("Expr []")
                    for i in obj:
                        self.recur_iter(i)


        elif type(obj) == str:
            if obj in self.vars_obj_list:
                return self.vars_obj_list[obj]
            
            elif obj in {"right", "left", "up", "down", "call", "endrepeat", "endif", "endproc", "repeat", "ifblock", "procedure", "set", "else", "*", "//", "-", "+", "^"}:
                print(obj)
                return obj

            else:
                print(f"Error - unknown name of variable or object: {obj}")
                self.json_data["Error"] = [f"unknown name of variable or object: {obj}"]


        elif type(obj) == Token:
            print(f"Get token - {obj.value}")
            return self.recur_iter(obj.value)


        elif type(obj) == int:
            return obj


        elif type(obj) == float:
            return obj
        
        elif type(obj) == dict:
            print(obj)

        else:
            print(f"Error - undefined object: {obj}")
            self.json_data['Error'] = [f"undefined object: {obj}"]


    def begin(self):

        if 'procedures' in self.data:
            procs = self.data['procedures']
            for proc in procs:
                keys = list(proc.keys())
                name = keys[0]
                self.vars_obj_list[name] = proc[name]['body']
            print(self.vars_obj_list)

        if "body" in self.data:
            self.main_body = self.data['body']
            print(self.main_body)
        
        self.recur_iter(self.main_body)
        

def comment_delete(text):
    all_lines = text.split("\n")
    for indx, line in enumerate(all_lines):
        s = ""
        for sym in line:
            if sym == "#":
                break
            s += sym
        all_lines[indx] = s
    return "\n".join(all_lines)
        

def run(text):
    text = comment_delete(text)
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    handler = Handler(tree)
    handler.begin()
    return handler.json_data
    








HOST = os.environ.get("HOST", default="http://localhost:8000/")
logging.basicConfig(level=logging.ERROR, filename="logging_mainapp.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
context_preview = None


def code_preview_convert(count, code_text):
        separated_strings = str(code_text).splitlines()
        return '\n'.join(separated_strings[:count])

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def filter_string(s):
    bad_chars = [';', ':', '!', "*", " ", '+', '-', '.']
    test_string = s
    for i in bad_chars:
        test_string = test_string.replace(i, '')
        
    return test_string


@login_required(login_url='login') 
def get_rendered_code(request):
    return JsonResponse(request.session['rendered_code'], safe=False)

@login_required(login_url='login') 
def code_editor(request, title): 
    request.session['title'] = title
    current_project = user_project.objects.get(title=title)
    code_content = current_project.file.read().decode('utf-8')
    title_content = current_project.title
    print(request.body)
    print(request.body)
    if request.method == 'POST':
        if request.content_type == 'application':
            if 'exit' in request.POST:
                print("exit")
                return redirect('project_manager')
            if 'save_and_exit_redirect' in f'{request.body}':
                return HttpResponseRedirect(reverse('project_manager'))
            
            else:
                print("OK")
                #return HttpResponseNotFound("Unknown POST request aplication") 
        
        if request.content_type in {'multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'}:
            print("Code editor / POST / JSON")
            print(loads(request.body))
            print(f'{request.content_type}, {request.body}')
            print(loads(request.body)["parent"])


            if 'save' in loads(request.body)['parent']:
                print("Code editor / POST / JSON / code")
                instance = user_project.objects.get(title=request.session['title1'])
                code1 = (json.loads((request.body).decode("utf-8"))['code'])
                print(code1)
                dir1 = ('media/'+str(instance.file))
                file_var = open(dir1, 'r')
                file_text_var = file_var.read()
                file_var.close()
                if code1 != file_text_var:
                    with open(dir1, "w", encoding="utf-8") as f:
                        f.write(code1)
                        f.close()

                size1 = os.path.getsize('media/'+str(instance.file))
                instance.size = size1
                instance.save()
                print('Size: ', size1)
        
        

            if 'save_and_exit_redirect' in loads(request.body)['parent']:
                
                print("Code editor / POST / JSON / save-and-exit")
                instance = user_project.objects.get(title=request.session['title1'])
                code1 = (json.loads((request.body).decode("utf-8"))['code'])
                print(code1)
                dir1 = ('media/'+str(instance.file))
                file_var = open(dir1, 'r')
                file_text_var = file_var.read()
                file_var.close()
                if code1 != file_text_var:
                    with open(dir1, "w", encoding="utf-8") as f:
                        f.write(code1)
                        f.close()

                size1 = os.path.getsize('media/'+str(instance.file))
                instance.size = size1
                instance.save()
                print('Size: ', size1)
      
            
            elif "start" in loads(request.body)["parent"]:
                try:
                    print(loads(request.body)["code"])
                    returned_data = run(loads(request.body)["code"])
                except Exception as error:
                    returned_data = {"Error": f"Syntaxis error in parser class, error log: {error}",}
                print(returned_data)
                request.session['rendered_code'] = dumps(returned_data)  
                          

            else:
                return HttpResponseNotFound("Unknown json") 
    
    return render(request, 'mainapp/code_editor.html', context={'code': code_content, 'title': title_content})


@login_required(login_url='login')
def project_manager(request):

    projects = user_project.objects.filter(creator=request.user)
    user = User.objects.filter(username=request.user)[0]
    date = timezone.now
    size = 0
    form = CreateProjectForm(initial={
                'creator': user.id,
                'date': date,
                'size': size,
            })
    
    if request.method == 'POST':
        print('POST: ', request.POST)
        file_update_flag = False
        print(1111) 
        print(request.content_type)
        if request.content_type in {'multipart/form-data',
                                    'application/x-www-form-urlencoded'}:
            print(2222)
            if 'create' in request.POST:     
                print(3333)
                if len(request.FILES) == 0:
                    print("4444a")
                    file_update_flag = True
                print("4444b")
                form = CreateProjectForm(request.POST, request.FILES)

                if form.is_valid():  
                    print(5555)
                    time_bound = form.save(commit=False)
                    time_bound.creator = user
                    request.session['title1'] = time_bound.title
                    print(6666)
                    if file_update_flag:
                        print(7777)
                        name = f'{time_bound.title}_{id_generator(6)}'
                        file_generate = open(f'{Path(__file__).resolve().parent.parent.parent}\gridmaster\media\codes\{name}', 'w+')
                        file_generate.write(f'# Created by {time_bound.creator}, on {time_bound.date.strftime("%b %d at %Y %H:%M:%S")}...')
                        time_bound.file = File(file=file_generate, name=f'{time_bound.title}_{id_generator(8)}')
                    print(8888)
                    same_titles = user_project.objects.filter(creator=time_bound.creator, title=time_bound.title)
                    
                    if len(same_titles) == 0:
                        print(9999)
                        time_bound.save()
                        file_var1 = open(f"media/{str(time_bound.file)}", 'r')
                        file_text_var1 = file_var1.read()
                        file_var1.close()
                        print(0000)
                        if file_update_flag:
                            file_generate.close()
                        print(11110)
                        request.session['file_text1'] = file_text_var1
                        instance = user_project.objects.get(title=request.session['title1'])
                        size1 = os.path.getsize('media/'+str(instance.file))
                        instance.size = size1
                        instance.save()
                        print(22220)
                        return redirect(user_project.objects.get(title=time_bound.title).get_absolute_url())
                    
                else:
                    print(form.errors)

            elif 'edit' in request.POST:
                return redirect(user_project.objects.get(title=request.session['title1']).get_absolute_url()) 

            elif 'delete' in request.POST:
                project = user_project.objects.get(title=request.session['title1'])
                file_name = project.file.name.replace("/", "\\")
                os.remove(f'{Path(__file__).resolve().parent.parent.parent}\gridmaster\media\{file_name}')
                project.delete()

            elif 'copy' in str(request.POST):
                print('COPY')
                form1 = CopyProject(request.POST, request.FILES)
                new_file_name = f'{request.session["title1"]}_copy_{id_generator(8)}'
                new_file_name = filter_string(new_file_name)+'.txt'

                if form1.is_valid():  
                    time_bound = form.save(commit=False)
                    time_bound.creator = user
                    time_bound.title = filter_string(new_file_name)[:-4]
                    time_bound.file = f'codes/{new_file_name}'
                    file = open(f'media/codes/{new_file_name}', 'w')
                    file.write(request.session['file_text1'])
                    file.close()
                    size1 = os.path.getsize('media/'+str(time_bound.file))
                    time_bound.size = size1
                    time_bound.description = request.session['description1']
                    time_bound.save()
                    instance = user_project.objects.get(title=request.session['title1'])
                    instance.save()
            
            else:
                print("OK")
                #return HttpResponseNotFound("Unknown POST request") 

    max_size = 5 * 1024
    cloud_percent = round(100 * (1-(sum([int(project.size) for project in projects]) / (max_size))), 1) 
    cloud_free_place = max_size - sum([int(project.size) for project in projects])
    flag_no_free_place = cloud_free_place <= 0

    try:
        tip = random.choice(all_tips.objects.all())
    except Exception:
        tip = None 

    context = {
        'cloud_percent': str(cloud_percent).replace(",", ".", 1),
        'cloud_free_place': cloud_free_place,
        'flag_no_free_place': flag_no_free_place,
        'tip': tip,
        'form': form,
        }

    if len(list(projects)) == 0:
        context['projects'] = None
    else:
        context['projects'] = projects
   
    return render(request, 'mainapp/project_manager.html', context)


def layout(request):
    return render(request, 'mainapp/layout_mainapp.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')
    

@login_required(login_url='login')
def code_preview(request):    
    global context_preview
    if request.method == "POST":
        title = loads(request.body)['title']
        request.session['title1'] = title
        code_preview_content_object = user_project.objects.get(title=title)
        converted_code_for_preview = code_preview_convert(20, code_preview_content_object.file.read().decode('utf-8'))
        request.session['description1'] = code_preview_content_object.description
        file_var = open(('media/'+ str(user_project.objects.get(title=request.session['title1']).file)), 'r')
        file_text_var = file_var.read()
        file_var.close()
        request.session['file_text1'] = file_text_var
        title = code_preview_content_object.title
        context_preview = { 'code_preview': converted_code_for_preview,
                    'title': title,
                    'date': str(code_preview_content_object.date).replace("-", "."),
                    'size': code_preview_content_object.size,
                    'description': code_preview_content_object.description,
                    'download_url': HOST + user_project.objects.get(title=title).file.url[1:],
                }
        
    if request.method == "GET":
        return JsonResponse(context_preview, safe=False)

    return HttpResponse("")




"""
elif 'code' in str(request.body):
    instance = user_project.objects.get(title=request.session['title1'])
    code1 = (json.loads((request.body).decode("utf-8"))['code'])
    print(code1)
    dir1 = ('media/'+str(instance.file))
    file_var = open(dir1, 'r')
    file_text_var = file_var.read()
    file_var.close()
    if code1 != file_text_var:
        with open(dir1, "w", encoding="utf-8") as f:
            f.write(code1)
            f.close()

    size1 = os.path.getsize('media/'+str(instance.file))
    instance.size = size1
    instance.save()
    print('Size: ', size1)
    pass
"""