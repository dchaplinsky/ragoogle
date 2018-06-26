document.addEventListener(
    "touchstart",
    function(){},
    true
);

$(function() {
    function populateBihusNews(data, $container, ntitle, link) {
        var title = data[0].title,
            nid = data[0].nid,
            teaser_text = data[0].field_teaser_text,
            created = data[0].created,
            big_teaser_media = data[0].field_teaser_media_1.replace(/^\s+|\s+$/g,''),
            declNews = '';

        declNews = declNews + '<div class="top-news"><a target="_blank" class="top-news-card" href="https://bihus.info/node/' + nid +'"><div class="news-block-title">Останні новини ' + ntitle + '</div>';
        declNews = declNews +  '<div class="top-news-container"><img src="' +  big_teaser_media +'" />';
        declNews = declNews +  '<div class="top-news-info"><h4>' + title  + '</h4>';
        declNews = declNews +  '<h6>' + created + '</h6><div class="top-teaser">' + teaser_text + '</div></div>';
        declNews = declNews + '</div></a></div>';

        declNews = declNews + '<div class="more-news"><div class="more-news-container">';

        for(i = 1; i < 6; i ++) {
            title = data[i].title,
                nid = data[i].nid,
                teaser_text = data[i].field_teaser_text,
                created = data[i].created,
                teaser_media = data[i].field_teaser_media;

            declNews = declNews +  '<a target="_blank" class="news-row" title="' + title +'" href="https://bihus.info/node/' + nid +'"><div class="media">';
            declNews= declNews + '<div class="media-left">';
            declNews= declNews + '<div class="media-object"><img src="' + teaser_media +'" />';
            declNews= declNews + '</div></div>';
            declNews= declNews + '<div class="media-body card-body">';
            declNews= declNews + '<div class="card-flip"><div class="face front"><h4 class="media-heading">' + title + '</h4>';
            declNews= declNews + '<h6>' + created + '</h6></div><div class="face back">' + teaser_text +'</div></div>';
            declNews= declNews + '</div></div></a>';
        }

        declNews = declNews + '<a target="_blank" href="' + link + '" class="more-news-more-link">Більше новин тут</a></div></div>';
        $($container).append(declNews);
    }

    function fetchBihusNews() {
        $('body').addClass('ajax-run');

        $.ajax({
            url: 'https://bihus.info/restapi/bihus-news',
            type: 'GET'
        })
            .done(function(data) {
                populateBihusNews(data, '#decl-bihus-block', 'Bihus.info', 'https://bihus.info/news/all');
            })
            .fail(function(event) {
                console.log(event.status);
            });
    }

    $(document).ajaxStop(function () {
        $('body').removeClass('ajax-run').addClass('bihus-news-ready');
    });

    $(document).ready(function() {
        if($('#newslist').length > 0) {
            fetchBihusNews();
        }
    });
});
