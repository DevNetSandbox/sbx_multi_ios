
function shouldHideSidebar() {
    if ($(window).width() < 992) {
        $('#appSidebar').addClass('sidebar--hidden');
    }
}
function doNav(url) {
    shouldHideSidebar();
    document.location.href = url;
}

$(document).ready(function() {

    // Wire the header sidebar toggle button
    $('#appHeader .toggle-menu').click(function () {
        $('#appSidebar').toggleClass('sidebar--hidden');
    });
    // Wire the sidebar drawer open/close toggles
    $('#appSidebar .sidebar__drawer > a').click(function() {
        $(this).parent().toggleClass('sidebar__drawer--opened');
    });

    // Wire the sidebar selected item
    $('#appSidebar .sidebar__item > a').click(function() {
        $('#appSidebar .sidebar__item').removeClass('sidebar__item--selected');
        $(this).parent().addClass('sidebar__item--selected');
    });
}
)
