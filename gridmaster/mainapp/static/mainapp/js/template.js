let isClose = true;

function userMenuToggle() {
    if (isClose == true) {
        userMenuOpen();
        return
    }
    userMenuClose();
}

function userMenuOpen() {
    let wrapper = document.querySelector('.account-menu__wrapper')
    wrapper.style.width = '19rem';

    let dots = document.querySelector('.account-menu__dots');
    dots.style.opacity = '0';
    let mainInfo = document.querySelector('.account-menu__main');
    mainInfo.classList.remove('show')
    let menuUser = document.querySelector('.account-menu__us-wrap');
    menuUser.style.marginLeft = '1.5rem'
    setTimeout(() => {
        wrapper.style.height = '12.6rem';
        menuUser.style.marginTop = '0.85rem'

        let avatar = document.querySelector('.account-menu__avatar');
        avatar.style.width = '2.8rem';
        avatar.style.height = '2.8rem';
        avatar.style.marginRight = '1.5rem'
        let name = document.querySelector(".account-menu__name");
        name.style.opacity = '1'

        setTimeout(() => {
            mainInfo.style.opacity = '1';

            isClose = false;
        }, 300)
    }, 600)
}

function userMenuClose() {
    let mainInfo = document.querySelector('.account-menu__main');
    mainInfo.style.opacity = '0';
    mainInfo.style.transition = '0.3s all ease'
    setTimeout(() => {
        mainInfo.classList.add('show')

        let wrapper = document.querySelector('.account-menu__wrapper')
        wrapper.style.height = '2.3rem';

        let avatar = document.querySelector('.account-menu__avatar');
        avatar.style.width = '1.8rem';
        avatar.style.height = '1.8rem';
        avatar.style.marginRight = '0.55rem'

        let name = document.querySelector(".account-menu__name");
        name.style.opacity = '0'

        let menuUser = document.querySelector('.account-menu__us-wrap');
        menuUser.style.marginLeft = '0'
        menuUser.style.marginTop = '0'

        setTimeout(() => {
            wrapper.style.width = '4.3rem'

            let dots = document.querySelector('.account-menu__dots');
            dots.style.opacity = '1';
            isClose = true;
        }, 600)
    }, 300)

}