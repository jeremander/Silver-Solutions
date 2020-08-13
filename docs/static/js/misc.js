// switch between subpages by clicking on links
$('.subpage-link').click(function() {
  const li = $(this).closest('li');
  const lis = $(this).closest('ul').children();
  const i = lis.index(li);
  lis.removeClass('active');
  li.addClass('active');
  window.localStorage.setItem('currentPageSection', i);
  const articles = $(this).closest('.info-page').find('article');
  $(articles.get(i))[0].scrollIntoView();
  const topbar = ($(window).width() <= 960) ? '.sidebar' : '#header';
  const offset = $(topbar).outerHeight() + 30;
  // compensate for nav bar height
  window.scrollBy(0, -offset);
});

// page section highlighting

function highlightCurrentPageSection() {
  const nav_links = $('.info-page .sidebar ul');
  const active_link = nav_links.find('.active')
  const i = window.localStorage.getItem('currentPageSection');
  // alert(i);
  const new_link = nav_links.children().get((i == null) ? 0 : i);
  active_link.removeClass('active');
  $(new_link).addClass('active');
}

function setupPageSectionObserver() {
  $('.info-page article').each(function() {
    $(this).prepend($('<div class="article-separator">'));
    $(this).append($('<div class="article-separator">'));
  });

  const topbar = ($(window).width() <= 960) ? '.sidebar' : '#header';
  const margin = $(topbar).outerHeight();

  function elementOverlapsMidpoint() {
    const rect = this.getBoundingClientRect();
    const height = $(window).height();
    const midpoint = margin + (height - margin) / 2.0;
    const margin_top = parseFloat($(this).css('marginTop'));
    const margin_bottom = parseFloat($(this).css('marginBottom'));
    return ((rect.top - margin_top <= midpoint) && (midpoint <= rect.top + rect.height + margin_bottom));
  };

  const observer = new IntersectionObserver(function(entries) {
    const target = entries[0].target;
    const article = $(target).parent();
    const articles = $(target).closest('.content').children();
    const overlaps = articles.map(elementOverlapsMidpoint);
    const i = overlaps.index(true);

    window.localStorage.setItem('currentPageSection', i);
    highlightCurrentPageSection();
  }, { threshold: [0.0, 0.1, 0.2, 0.3] });

  const observe = function() {
    observer.observe(this);
  }

  $('.info-page article').each(observe);
  $('.info-page .article-separator').each(observe);
}

$("#contact form").submit(function(e) {
  e.preventDefault();

  const contact = $('#contact')

  $.ajax({
    url: 'https://formspree.io/xjvaevaz',
    method: 'POST',
    data: {
      name: contact.find('#contact-name input').val(),
      _replyto: contact.find('#contact-email input').val(),
      message: contact.find('#contact-message textarea').val(),
    },
    dataType: "json",
    success: function() {
      $('#submit-success').fadeIn(700, function () {
        contact.find('textarea').val('');
        contact.find('input').val('');
      }).delay(1200).fadeOut(700);
    }
  });
});

$(document).ready(function() {
  highlightCurrentPageSection();

  // delay loading the second & third banner images

  $('.banner1').delay(3000).queue(function(next) {
    $(this).css('visibility', 'visible')
    next();
  });

  $('.banner2').delay(7500).queue(function (next) {
    $(this).css('visibility', 'visible');
    next();
  });
});