'use strict';

var animationDuration;

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
}

function sem2words(sem) {
    var sems = {"1": "first", "2": "second", "3": "third", "4": "fourth", "5": "fifth", "6":"sixth", "7":"seventh", "8": "eighth"};
    return sems[sem];
}

function load_profile(data) {
    document.getElementById("enrolment_number").innerHTML = data.enrolment_number;
    document.getElementById("name").innerHTML = toTitleCase(data.name);
    document.getElementById("institute").innerHTML = toTitleCase(data.college);
    var course = /(.*)\((.*)\)/.exec(data.course);
    document.getElementById("programme").innerHTML = toTitleCase(course[1]);
    document.getElementById("stream").innerHTML = toTitleCase(course[2]);
}

function calculate_last_sem(data) {
    var percent = 0;
    for (var index = 0; index < results.length; index++) {
        if (!isNaN(results[index].total.replace('*', ''))) {
            var total = parseInt(results[index].total);
            percent += total;
        }
    }
    percent = Math.round(percent / results.length);
    return percent;
}

function update_table(results) {
    var html = "", percent = 0, back = 0, max = ["", "", 0], min = ["", "", 101];
    for (var index = 0; index < results.length; index++) {
        html += "<tr>";
        html += "<td class='hidden-xs hidden-sm'>" + results[index].code + "</td>";
        html += "<td>" + results[index].name + "</td>";
        html += "<td class='text-center hidden-xs hidden-sm'>" + results[index].internal + "</td>";
        html += "<td class='text-center hidden-xs hidden-sm'>" + results[index].external + "</td>";
        html += "<td class='text-center'>" + results[index].total + "</td>";
        if (results[index].status == '0') {
            back += 1;
            html += "<td class='text-center'x><i class='zmdi zmdi-circle zmdi-hc-fw text-danger'></i></td>";
        } else {
            html += "<td class='text-center'>" + results[index].credits + "</td>";
        }
        html += "</tr>";
        if (!isNaN(results[index].total.replace('*', ''))) {
            var total = parseInt(results[index].total);
            percent += total;
            if (total > max[2]) {
                max[0] = results[index].code;
                max[1] = results[index].name;
                max[2] = total;
            }
            if (total < min[2]) {
                min[0] = results[index].code;
                min[1] = results[index].name;
                min[2] = total;
            }
        }

    }

    // var subjectCodeHTML = "<span data-toggle='tooltip' data-placement='bottom' title='Tooltip on bottom'>$</span>";

    document.getElementById('sem-table-body').innerHTML = html;
    percent = Math.round(percent / results.length);
    $('#this-sem-percent').data('easyPieChart').update(percent);
    $('#subjects-cleared').data('easyPieChart').update(Math.round(100 - (back / results.length) * 100));
    $('#best-subject').data('easyPieChart').update(max[2]);
    $('#best-subject-code').html(max[0]);
    $('#worst-subject').data('easyPieChart').update(min[2]);
    $('#worst-subject-code').html(min[0]);

    var noback = ["You passed motherfucker!!", "Holy Grail! No fuckin backs", "Wait... How the fuck you didn't fail?", "No Backs Bastard"]
    var yesback = ["Go Die! You fuckin failed in $ subject(s)", "Sorry You flunked in $", "Ha Ha Ha! You got $ motherfuckin back(s)"]
    var text = ""
    if (back == 0)
        text = noback[Math.floor(Math.random() * noback.length)];
    else
        text = yesback[Math.floor(Math.random() * yesback.length)].replace('$', back);
    document.getElementById("header-text").innerHTML = text;
}

function getSemesterResult(sem) {
    var data = JSON.parse(sessionStorage.getItem("data"));
    sessionStorage.setItem("sem", sem);
    update_table(data.results[sem]);
}

function loadPage(type) {
    var data = JSON.parse(sessionStorage.getItem("data"));
    // console.log(data);    
    if (type == 'latest') {
        var sems = $.map(data.results, function (value, key) {
            return key;
        });
        var sem = Math.max.apply(Math, sems).toString();
        sessionStorage.setItem("latest",sem);
        // -----------------------------------------------------
        if (sem == "1")
            $("#previous-sem").hide();
        $("#next-sem").hide();
        // -----------------------------------------------------
        load_profile(data);
        getSemesterResult(sem);

    } else {
        getSemesterResult(type);
        $("#next-sem").show();
        $("#previous-sem").show();
        $("#sem-header").html("Motherfuckin " + sem2words(type) + " semester");
    }
}

$(document).ready(function () {
    sessionStorage.clear();
    $("#eno").on('keyup', function (e) {
        if (e.keyCode == 13) {
            $("#arrow-button").click();
        }
    });

    $('body').on('click', '.animation-demo .btn', function () {
        var animation = $(this).data("animation");
        var enrolBox = $(this).closest('.login__block')
        if (animation === "hinge") {
            animationDuration = 2100;
        }
        else {
            animationDuration = 1500;
        }
        enrolBox.removeAttr('class');
        enrolBox.addClass('animated ' + animation);
        var eno = document.getElementById('eno').value;
        setTimeout(function () {
            var url = 'http://myipuresult.com/api.php/result/' + eno;
            var page2 = $('#main');
            page2.css('visibility', 'visible');
            page2.removeAttr('class');
            page2.addClass('animated ' + page2.data('animation'));

            $.getJSON(url, function (data) {
                sessionStorage.setItem("data", JSON.stringify(data));
                loadPage('latest');
            }).error(function (data, textStatus, errorThrown) {
                var dataJSON = JSON.parse(data.responseText);
                swal({
                    title: "I'm Afraid but...",
                    text: dataJSON.error_description,
                    type: "warning",
                    confirmButtonText: "Fuck!"
                }).then(function () {
                    location.reload();
                });
            });
        }, animationDuration / 2);
    });

    $('.chart-pie').each(function () {
        var value = $(this).data('pie-value');
        var size = $(this).data('pie-size');

        $(this).find('.chart-pie__value').css({
            lineHeight: (size - 2) + 'px',
            fontSize: (size / 4) + 'px'
        });

        $(this).easyPieChart({
            easing: 'easeOutBounce',
            barColor: 'rgba(255,255,255,0.6)',
            trackColor: '#22313a',
            scaleColor: 'rgba(0,0,0,0)',
            lineCap: 'round',
            lineWidth: 2,
            size: size,
            animate: 3000,
            onStep: function (from, to, percent) {
                $(this.el).find('.chart-pie__value').text(Math.round(percent));
            }
        })
    });

    $('#previous-sem').on('click', function () {
        var sem = parseInt(sessionStorage.getItem('sem')) - 1;
        if (sem < 1)
            sem = 1;
        loadPage(sem.toString());
        if (sem == "1")
            $("#previous-sem").hide();
    });

    $('#next-sem').on('click', function () {
        var sem = parseInt(sessionStorage.getItem('sem')) + 1;
        var max = parseInt(sessionStorage.getItem("latest"));
        if (sem > max)
            sem = max;
        loadPage(sem.toString());
        if (sem >= max){
            $("#next-sem").hide();
            $("#sem-header").html("This motherfuckin Semester");
        }
    });
});

