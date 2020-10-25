// remove all but the first three sections from top navbar when window is narrow
// merge samples & testimonials to consolidate space
function setupSubpageLinks() {
  const isMobile = $(window).width() <= 552;
  const links = $('.sidebar').find('li');
  for (i = 0; i < links.length; ++i) {
    let link = links.get(i);
    if (isMobile) {
      if (link.textContent == 'Samples') {
        $(link).children('a')[0].textContent = 'Samples & Testimonials';
      }
      if (i > 2) {
        $(link).hide();
      }
      window.localStorage.setItem('numVisibleLinks', Math.min(3, links.length));
    }
    else {
      if (link.textContent == 'Samples & Testimonials') {
        $(link).children('a')[0].textContent = 'Samples';
      }
      $(link).show();
      window.localStorage.setItem('numVisibleLinks', links.length);
    }
  }
}

$(window).resize(setupSubpageLinks);

function highlightPageSection(i) {
  const nav_links = $('.info-page .sidebar ul');
  const active_link = nav_links.find('.active');
  const new_link = nav_links.children().get((i == null) ? 0 : i);
  active_link.removeClass('active');
  $(new_link).addClass('active');
  window.localStorage.setItem('currentPageSection', i);
  window.localStorage.setItem('pageSectionRefresh', 1);
}

// page section highlighting
function highlightCurrentPageSection() {
  const i = window.localStorage.getItem('currentPageSection');
  highlightPageSection(i);
}

// switch between subpages by clicking on links
$('.subpage-link').click(function () {
  const li = $(this).closest('li');
  const lis = $(this).closest('ul').children();
  const i = lis.index(li);
  // lis.removeClass('active');
  // li.addClass('active');
  // window.localStorage.setItem('currentPageSection', i);
  const articles = $(this).closest('.info-page').find('article');
  $(articles.get(i))[0].scrollIntoView();
  const topbar = ($(window).width() <= 960) ? '.sidebar' : '#header';
  const offset = $(topbar).outerHeight() + 30;
  // compensate for nav bar height
  window.scrollBy(0, -offset);
  highlightPageSection(i);
  // signal not to refresh the page section since we just set it manually
  window.localStorage.setItem('pageSectionRefresh', 0);
});

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
    let i = overlaps.index(true);
    let shouldRefresh = window.localStorage.getItem('pageSectionRefresh');
    let numVisibleLinks = window.localStorage.getItem('numVisibleLinks');
    if (shouldRefresh == 1) {
      if (i >= numVisibleLinks) {
        i = numVisibleLinks - 1;
      }
      highlightPageSection(i);
    }
    window.localStorage.setItem('pageSectionRefresh', 1);
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
  setupSubpageLinks();
  highlightCurrentPageSection();

  // delay loading the second & third banner images

  $('.banner1').delay(3000).queue(function(next) {
    $(this).css('visibility', 'visible')
    $(this).children().css('visibility', 'visible');
    next();
  });

  $('.banner2').delay(7500).queue(function (next) {
    $(this).css('visibility', 'visible');
    $(this).children().css('visibility', 'visible');
    next();
  });
});