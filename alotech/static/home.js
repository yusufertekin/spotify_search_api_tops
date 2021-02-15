$(document).ready(function () {
  $("#search-button").click(function () {
    var genre = $("#search-input").val();
    $("#track-list").hide();
    $("#loading-gif").show();
    $.get(
      `/tracks/${genre}`,
      function (response) {
        $("#track-list").empty();
        response.forEach(function (track) {
          $("#track-list").append(
            `<div class="track-box">
              <img
                class="album-image"
                src="${track.album_image_url}" />
              <div class="description">
                <strong>${track.track}</strong>
                <strong>${track.artist}</strong>
              </div>
              <div class="preview">
              </div>
             </div>`
          );
          if (track.preview_url) {
            $("#track-list .track-box:last-child .preview").append(
              `<video class="preview-video" controls="" name="media">
                  <source
                    src="${track.preview_url}"
                    type="audio/mpeg">
                </video>`
            );
          } else {
            $("#track-list .track-box:last-child .preview").append(
              "<span>There is no preview</span>"
            );
          }
        });
      }
    ).fail(function (response) {
      $("#ajax-error").html(`${response.responseJSON.message}`);
      $("#ajax-error").show();
      setTimeout(function () {
        $("#ajax-error").hide();
      }, 5000);
    })
    .always(function () {
      $("#track-list").show();
      $("#loading-gif").hide();
    });
  });
});
