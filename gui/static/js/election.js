$(function () {
    $(document).ready(function () {

    });

    var most_common_videos = null;
    //ajax method for loading title search in welcome fetches experiments
    $.ajax({
        url: '/title_welcome_fetch',
        type: 'GET',
        success: function (response) {
            let title_element = $("#title-fig1");

            let dates_arr = response.date.split("/")
            let dates_str = dates_arr[1] + "/" + dates_arr[0] + "/" + dates_arr[2]

            title_element.text(`Hier, le ${dates_str}, les recommandations politiques observées sur la page d'accueil
            de YouTube (${response.political_mention} sur ${response.total_videos} au total) parlaient de:`);

            let i = 1;
            most_common_videos = response.most_common_videos
            for (const k in response.data) {
                // let number = parseInt(response[k] * 100) + "%";
                let number = (response.data[k] * 100).toFixed(1) + "%";
                if (number === "0.0%") {
                    number = "0%";
                }
                $("#welcome-fetch-title-ratio").append("<div class=\"col-lg-2 \">" +
                    "                    <img id=\"avatar" + k + "\" class=\"rounded-circle candidate-avatar z-depth-2\" alt=\"100x100\"" +
                    "                         src=\"static/images/avatars/" + k + ".jpg\"" +
                    "                         data-holder-rendered=\"true\">" +
                    "                    <h2>" + k + "</h2>" +
                    "                    <h2>" + number + "</h2>" +
                    "                </div><!-- /.col-lg-4 -->");
                // $("#avatar"+k).data(response.most_common_videos)
                // if (i === Math.floor(Object.keys(response).length / 2)) {
                //     $("#welcome-fetch-title-ratio").append("  <div class=\"w-100\"></div>");
                // }
                i += 1;
            }

            $(".candidate-avatar").click(function () {

                let candidateName = this.id.replace("avatar", "");
                $("#topVideosModalLabel").text(`Les vidéos de ${candidateName} les plus recommandées:`);
                var videos = most_common_videos[candidateName]
                $("#modal-list-group").empty()
                for (const video of videos) {

                    $("#modal-list-group").append("<a href=" + video[1] + " target=\"_blank\" rel=\"noopener noreferrer\" >\n" +
                        "                    <li class=\"list-group-item d-flex justify-content-between align-items-center\">" + video[0] +
                        "                        <span class=\"badge bg-primary rounded-pill\">" + video[2] + "</span>\n" +
                        "                    </li></a>")


                }

                $('#topVideosModal').modal('show')
            });
        }
    });

    //ajax method for loading csa vs transcript duration comparison in welcome walks experiments
    $.ajax({
        url: '/csa_transcript_duration',
        type: 'GET',
        success: function (response) {
            source = ["Youtube", "Media (Declared)"]
            response.data.forEach(function (x) { // Default sources are named as Youtube and CSA
                if (x.source === "CSA") {
                    x.source = "Media (Declared)"
                }
            });

            chart = GroupedBarChart(response.data, {
                x: d => d.candidate,
                y: d => d.ratio,
                z: d => d.source,
                xDomain: response.candidates,//d3.groupSort(stateages, D => d3.sum(D, d => -d.population), d => d.state),
                yLabel: "↑ Ratio (percentage)",
                zDomain: source,
                colors: d3.schemeSpectral[source.length],
                width: 1200,
                height: 500
            })
            chart.style.overflow = "visible";
            let key = Swatches(chart.scales.color, {title: "Source", swatchSize: 20});

            // let key = Legend(chart.scales.color, {title: "Source"}) // try also Swatches
            key.style.display = "block";


            $("#csa_transcript_duration").html(key);
            $("#csa_transcript_duration").append(chart);
        }
    });

    // $.ajax({
    //     url: '/transcript_welcome_walk_over_time',
    //     type: 'GET',
    //     success: function (response) {
    //         candidate = response.candidates
    //         chart = LineChart(response.data, {
    //             x: d => new Date(d.date),
    //             y: d => d.ratio,
    //             z: d => d.candidate,
    //             yLabel: "↑ Transcript Duration (%)",
    //             width: 1200,
    //             height: 500,
    //             color: d3.scaleOrdinal(d3.schemeCategory10),
    //             // yType: d3.scaleOrdinal
    //         })
    //         chart.style.overflow = "visible";
    //         let key = Swatches(d3.scaleOrdinal(candidate, d3.schemeCategory10),{marginLeft:"5px"});
    //         key.style.width="630px"
    //         key.style.marginBottom="30px"
    //         // let key = Legend(chart.scales.color, {title: "Source"}) // try also Swatches
    //         // key.style.display = "inline-flex"
    //         // let key = Swatches(chart.scales.colors)
    //         key.style.display = "inline-flex"
    //         $("#transcript-welcome-walk-over-time-chart").html(key);
    //         $("#transcript-welcome-walk-over-time-chart").append(chart);
    //
    //         // $("#csa_transcript_duration").append(chart);
    //     }
    // });


});