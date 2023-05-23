var analysis = null
var paintScaledFactor = 1
var bboxColors = {}


/* message */

function sendMsg(msg) {
  if (msg) {
    let html = $(".msg.to.hide").clone();
    html.removeClass('hide');
    html.find('p').text(msg);
    html.insertBefore("#typing-msg");

    $("#inputtext").val('');
    $('#typing-msg').removeClass('hide');
    $(".chat .body").animate({ scrollTop: $('.chat .body').prop("scrollHeight")}, 300);
  }
}

function receiveMsg(msg, borderColor = null) {
  if (msg) {
    let html = $(".msg.from.hide:first").clone();
    html.removeClass('hide');
    html.find('p').text(msg);
    if (borderColor != null)
      html.find('.text').attr('style', `border-color: #${borderColor};`)
    html.insertBefore("#typing-msg");

    $('#typing-msg').addClass('hide');
    $(".chat .body").animate({ scrollTop: $('.chat .body').prop("scrollHeight")}, 300);
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
    style += `border-color: #${color}`

    // clone and set property
    let lazo = $(".lazo:first").clone();
    lazo.removeClass('hide');
    lazo.attr('style', style)
    lazo.attr('data-index', index)
    lazo.on('click', bboxClickEvent)

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
  console.log(area)

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
      receiveMsg("This is what I found. Click on a box to find out all the details.")
    },
    statusCode: {
    404: function() {
        receiveMsg("Sorry, I didn't find anything..☹️ Try again. ")
      }
    }
  })
}

/* DOM events */

function bboxClickEvent() {
  let index = $(this).attr('data-index')
  let start_end_pos = analysis.segments[index].start_end_pos
  let text = analysis.desc.substring(start_end_pos.start, start_end_pos.end)

  let keyColor = getKeyColor(start_end_pos)
  let color = bboxColors[keyColor]

  receiveMsg(text, color)
}

function sendBtnClick() {
  let title = $("#inputtext").val();
  sendMsg(title);
  makeAnalysis(title)
}

function pointerBtnClick() {
  // clear older bbox
  $('.bboxes .lazo').not('.hide').remove()

  // TODO take point on image and send to server

  // get image
  let img = $('.paint img')
  img = img[0]

  // print analysis
  printAnalysis(img)
}

$(document).ready(function() {
  $("#sendbtn").click(function (){
    sendBtnClick();
  });

  $("#pointerbtn").click(function (){
    pointerBtnClick();
  });

  $("#inputtext").keypress(function (e) {
    var code = (e.keyCode ? e.keyCode : e.which);
    if (code == 13) { // enter button
      sendBtnClick()
      return false;
    }
  });

  $(window).on( "resize", function() {
    console.log('RESIZE')
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
