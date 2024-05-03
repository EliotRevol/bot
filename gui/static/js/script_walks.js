const TIMEOUT_SECONDS = 600000 * 5;
const NB_WALKS = 5;
$(function () {
    let run_walk_btn = "#run-walk";
    $(run_walk_btn).click(function () {
        let $inputUrl = $("#inputUrl");
        if ($inputUrl.val()!="") {
            $(run_walk_btn).prop("disabled", true);
            $inputUrl.prop("readonly",true);
            function reset_call($progress, currentAjax, timeout) {
                $(run_walk_btn).prop("disabled", false);
                $inputUrl.prop("readonly",true);
                $progress.css("display", 'none');
                currentAjax = null;
                clearTimeout(timeout)
                return currentAjax;
            }

            $("#channel-videos-result").html("Fetching channel videos");

            $.ajax({
                url: '/channelSniff',
                data: $('#form-parameters').serialize(),
                type: 'POST',
                success: function (response) {

                    let currentAjax;
                    console.log(response);
                    $("#channel-videos-result").html("Fetched channel videos");


                    let params = $('#form-parameters').serializeArray();
                    params.push({name: 'channel_videos', value: JSON.stringify(response.channel_videos)});
                    params.push({name: 'channel_name', value: response.channel_name});

                    let nbWalks = NB_WALKS;
                    let $progress = $("#progress-bar");
                    let timeout = setTimeout(function () {
                        currentAjax.abort();
                        $("#channel-videos-result-timeout").html("Timeout after " + TIMEOUT_SECONDS + " seconds");
                        currentAjax = reset_call($progress, currentAjax, timeout);


                    }, TIMEOUT_SECONDS);
                    $progress.css("display", 'flex');
                    currentAjax = null;
                    $("#channel-videos-result").html("Started walks");

                    walk(nbWalks);

                    // sendRequests([1, 2, 3, 4]);
                    function walk(walkIterNb) {
                        currentAjax = $.ajax({
                            url: '/walk_iter',
                            data: params,
                            type: 'POST',
                            dataType: 'json',
                            success: function (response) {
                                let li_html = '<li className="list-group-item"><a href="' + response.csv_path + '">' + response.search_term + '</a></li>';
                                $("#csv-list").append(li_html);
                                console.log(response);
                                let currentIter = nbWalks - walkIterNb + 1;
                                $("#channel-videos-result").html("Fetched channel videos, walk: " + currentIter);
                                $progress.css("width", String(100 * currentIter / nbWalks) + "%");


                                if (currentIter < nbWalks) {
                                    walk(walkIterNb - 1);
                                } else {
                                    currentAjax = reset_call($progress, currentAjax, timeout);
                                }

                            },
                            error: function (error) {
                                console.log(error);
                                $("#channel-videos-result-timeout").html("Error: " + error);
                                currentAjax = reset_call($progress, currentAjax, timeout);

                            }
                        });

                    }

                },
                error: function (error) {

                    $("#channel-videos-result-timeout").html("Error: " + error);
                    console.log(error);
                    currentAjax = reset_call($progress, currentAjax, timeout);

                }
            });
        }
    });
});