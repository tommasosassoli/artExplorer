var analysis = null
var paintScaledFactor = 1
var bboxColors = {}


/* message */

function sendMsg(msg) {
  if (msg) {
    $("#inputtext").val('');
    $('#art-desc').addClass('hide').html('');
    $('#notfound-popup').addClass('hide');
    $('#idle-popup').removeClass('hide').find('.loading').removeClass('hide');
  }
}

function receiveMsg(msg) {
  if (msg) {
    $('#idle-popup').addClass('hide').find('.loading').addClass('hide');
    $('#notfound-popup').addClass('hide');
    $('#art-desc').removeClass('hide').html(msg);
  } else {
    $('#idle-popup').addClass('hide').find('.loading').addClass('hide');
    $('#notfound-popup').removeClass('hide');
  }
}

/* image and bboxes */

function getContainedSize(img) {
  var ratio = img.naturalWidth/img.naturalHeight
  var width = img.height*ratio
  var height = img.height
  if (width > img.width) {
    width = img.width
    height = img.width/ratio
  }
  return [width, height]
}

function getScaledFactor(img) {
  let dim = getContainedSize(img)
  let cWidth = dim[0]
  return cWidth / img.naturalWidth
}

function getKeyColor(start_end_pos) {
  return start_end_pos.start + '-' + start_end_pos.end
}

function printBbox(bbox, index) {
  if (bbox) {
    // bbox dimension and position
    let top = bbox.startY * paintScaledFactor
    let left = bbox.startX * paintScaledFactor
    let width = (bbox.endX - bbox.startX) * paintScaledFactor
    let height = (bbox.endY - bbox.startY) * paintScaledFactor

    let style = `top: ${top}px; left: ${left}px; width: ${width}px; height: ${height}px;`

    // bbox color
    let start_end_pos = analysis.segments[index].start_end_pos
    let keyColor = getKeyColor(start_end_pos)
    if (bboxColors[keyColor] === undefined) {
      let color = Math.floor(Math.random()*16777215).toString(16);
      bboxColors[keyColor] = color
    }
    let color = bboxColors[keyColor]
    style += `border-color: #${color}; opacity: 0.3;`

    // clone and set property
    let lazo = $(".lazo:first").clone();
    lazo.removeClass('hide');
    lazo.attr('style', style)
    lazo.attr('data-index', index)
    lazo.attr('data-key-color', keyColor)
    lazo.hover(bboxHoverInEvent, bboxHoverOutEvent)
    //lazo.on('mouseenter', bboxHoverInEvent)

    $('.bboxes').append(lazo)
  }
}

function setBboxZIndex() {
  // calc areas
  let area = []
  analysis.segments.forEach((item, index) => {
    let box = item.bbox
    let width = box.endX - box.startX
    let height = box.endY - box.startY
    let a = {'index': index, 'area': width * height}
    area.push(a)
  })
  area.sort((first, second) => second.area - first.area)

  // z ordering
  const offset = 3  // z-index starting offset
  area.forEach((item, index) => {
    $('.lazo[data-index=' + item.index + ']').css('z-index', index)
  })
}

function printAnalysis(img) {
  // calc bbox container dimensions
  let dim = getContainedSize(img)
  $('.bboxes').attr('style', `width: ${dim[0]}px; height: ${dim[1]}px;`)

  // calc the scaled factor of the image (from natural size) and print bboxes
  paintScaledFactor = getScaledFactor(img)
  analysis.segments.forEach((item, index) => printBbox(item.bbox, index))
  setBboxZIndex()
}

/* description and text */

function splitDescription(analysis) {
  let desc = analysis.desc
  let text_pos = analysis.segments.map(function(s) {
    return getKeyColor(s.start_end_pos)
  })
  text_pos = [...new Set(text_pos)].sort()

  let html_desc = ''
  text_pos.forEach((val, index) => {
    let spl = val.split('-')
    let start = parseInt(spl[0])
    let stop = parseInt(spl[1])
    let color = '#' + bboxColors[val] + '30' // last value is for background opacity

    html_desc += '<span class="highlight" ' +
        'style="background-color: ' + color + ';" ' +
        'data-index="' + index + '" ' +
        'data-key-color="' + val + '">' +
        desc.substring(start, stop) + '</span>'
  })
  return html_desc
}

/* ajax calls */

function makeAnalysis(title) {
  $.ajax({
    url: '/' + encodeURI(title),
    datatype: 'json',
    success: function (result) {
      analysis = result

      // set image url
      let img = $('.paint img')
      img.attr('src', analysis.img_url)
      img = img[0]

      // clear older bbox
      $('.bboxes .lazo').not('.hide').remove()
      bboxColors = {}
      $('.chat .msg.from').find('.text').removeAttr('style')

      printAnalysis(img)
      let descHtml = splitDescription(analysis)
      receiveMsg(descHtml)
      // set event
      $('.highlight').hover(bboxHoverInEvent, bboxHoverOutEvent)
    },
    statusCode: {
    404: function() {
        receiveMsg(null)
      }
    }
  })
}

/* DOM events */

function bboxHoverInEvent() {
  let keyColor = $(this).attr('data-key-color')
  bboxHoverEvent(keyColor, '80')
}

function bboxHoverOutEvent() {
  let keyColor = $(this).attr('data-key-color')
  bboxHoverEvent(keyColor, '30')
}

function bboxHoverEvent(keyColor, opacity) {
  let span = $('.highlight[data-key-color="' + keyColor + '"]')[0]
  let color  = '#' + bboxColors[keyColor];
  color += opacity
  $(span).css('backgroundColor', color)

  let lazo = $('.lazo[data-key-color="' + keyColor + '"]')
  lazo.css('opacity', opacity / 100)
}

function sendBtnClick() {
  let title = $("#inputtext").val();
  sendMsg(title);
  makeAnalysis(title)
}

$(document).ready(function() {
  $("#sendbtn").click(function (){
    sendBtnClick();
  });

  $("#inputtext").keypress(function (e) {
    var code = (e.keyCode ? e.keyCode : e.which);
    if (code == 13) { // enter button
      sendBtnClick()
      return false;
    }
  });

  $(window).on( "resize", function() {
    // clear older bbox
    $('.bboxes .lazo').not('.hide').remove()

    // get image
    let img = $('.paint img')
    img = img[0]

    // print analysis
    printAnalysis(img)
  });

  // $(".paint img").on("click", function(event) {
  //       var x = event.pageX - this.offsetLeft;
  //       var y = event.pageY - this.offsetTop;
  //       alert("X Coordinate: " + x + " Y Coordinate: " + y);
  //   });
});
