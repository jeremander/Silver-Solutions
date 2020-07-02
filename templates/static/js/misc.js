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
  const offset = $(topbar).outerHeight() + 12;
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
  const observer = new IntersectionObserver(function(entries) {
    const target = entries[0].target;
    // alert(target);
    if (entries[0].isIntersecting) {
      const i = $(target).closest('.content').children().index(target);
      window.localStorage.setItem('currentPageSection', i);
      highlightCurrentPageSection();
    }
  }, { threshold: [0.5] });

  $('.info-page article').each(function() {
    observer.observe(this);
  });
}

$(document).ready(function() {
  highlightCurrentPageSection();
});