/**
 * Created by kecorbin on 11/11/17.
 */

// display a loading graphic while resources are being loaded
function href_with_loader(url) {
    $('#main-panel-content').hide();
    $('#loading').show();
    window.location.href = url;
}