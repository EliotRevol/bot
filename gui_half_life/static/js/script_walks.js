const TIMEOUT_SECONDS = 600000 * 5;
// const TIMEOUT_SECONDS = 6000;

const NB_WALKS = 5;
$(function () {
    let run_walk_btn = "#run-walk";
    var timeout = null;
    var $progress = $("#progress-bar");

    $(run_walk_btn).click(function () {
        let $inputUrl = $("#inputUrl");
        if ($inputUrl.val() != "") {
            $(run_walk_btn).prop("disabled", true);
            $inputUrl.prop("readonly", true);

            function reset_call($progress, currentAjax, timeout) {
                $(run_walk_btn).prop("disabled", false);
                $inputUrl.prop("readonly", false);
                $progress.css("display", 'none');
                currentAjax = null;
                clearTimeout(timeout)
                return currentAjax;
            }

            function remove_videos() {
                $("#csv-list").empty();

            }
            remove_videos()
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
                    if (timeout) {
                        clearTimeout(timeout);
                        timeout = null;
                    }
                    timeout = setTimeout(function () {
                        currentAjax.abort();
                        $("#channel-videos-result-timeout").html("Timeout after " + TIMEOUT_SECONDS + " seconds");
                        currentAjax = reset_call($progress, currentAjax, timeout);


                    }, TIMEOUT_SECONDS);
                    $progress.css("display", 'flex');
                    currentAjax = null;
                    $("#channel-videos-result").html("Started walks");

                    var iProgressBar = 0;

                    function makeProgress() {
                        if (iProgressBar < 99) {
                            iProgressBar = iProgressBar + 1;
                            $progress.css("width", iProgressBar + "%")
                        }

                        // Wait for sometime before running this script again
                        setTimeout(makeProgress, 15000);//150000 seconds
                    }

                    makeProgress();


                    walk();

                    // sendRequests([1, 2, 3, 4]);
                    function walk() {
                        currentAjax = $.ajax({
                            url: '/walk_iter',
                            data: params,
                            type: 'POST',
                            dataType: 'json',
                            success: function (response) {
                                for (const responseElement of response.videos) {

                                    let li_html = '<li className="list-group-item"><a href="https://www.youtube.com/watch?v=' + responseElement['video_id'] + '">' + responseElement['searchTerm'] + '</a></li>';
                                    $("#csv-list").append(li_html);
                                }


                                chart = LineChart(response.distances, {
                                    x: d => d.step,
                                    y: d => d.value,
                                    z: d => d.type,
                                    yLabel: "Cosine Similarity (%)",
                                    xLabel: "Step",
                                    xType: d3.scaleLinear,

                                    width: 960,
                                    height: 600,
                                    color: d3.scaleOrdinal(d3.schemeCategory10),
                                    numeric_x: true
                                    // yType: d3.scaleOrdinal
                                })
                                chart.style.overflow = "visible";
                                let key = Swatches(d3.scaleOrdinal(["Reference", "Walk"], d3.schemeCategory10), {marginLeft: "5px"});
                                key.style.width = "630px"
                                key.style.marginBottom = "30px"
                                // let key = Legend(chart.scales.color, {title: "Source"}) // try also Swatches
                                // key.style.display = "inline-flex"
                                // let key = Swatches(chart.scales.colors)
                                key.style.display = "content"
                                $("#cosine-chart").html(key);
                                $("#cosine-chart").append(chart);
                                $("#channel-videos-result").html("Calculated cosine distance");

                                console.log(response);
                                // let currentIter = nbWalks - walkIterNb + 1;
                                // $("#channel-videos-result").html("Fetched channel videos, walk: " + currentIter);
                                // $progress.css("width", String(100 ) + "%");
                                // if (currentIter < nbWalks) {
                                //     walk(walkIterNb - 1);
                                // } else {
                                currentAjax = reset_call($progress, currentAjax, timeout);
                                // }
                            },
                            error: function (error) {
                                console.log(error);
                                $("#channel-videos-result-timeout").html("Error, try again later...");
                                currentAjax = reset_call($progress, currentAjax, timeout);
                                remove_videos()
                                // $("#channel-videos-result").html("Fetched channel videos");

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