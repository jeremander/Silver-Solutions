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
  // const content = $('.info-page .content');
  const offset = parseInt($('.info-page .content').css('padding-top'), 10);
  // scrolls a little too far, so back up
  window.scrollBy(0, -(offset + 10));
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

// change the sidebar display when the top navbar goes in/out of view
const navbar_observer = new IntersectionObserver(function(entries) {
  const info_page = $('.info-page');
  if (entries[0].isIntersecting) {
    info_page.removeClass('nav-invisible');
    info_page.addClass('nav-visible');
  }
  else {
    info_page.removeClass('nav-visible');
    info_page.addClass('nav-invisible');
  }
}, { threshold: [0] });

navbar_observer.observe(document.querySelector('#nav'));

$(document).ready(function() {
  highlightCurrentPageSection();
});