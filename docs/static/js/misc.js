// switch between subpages by clicking on links
$('.subpage-link').click(function() {
  const li = $(this).closest('li');
  const lis = $(this).closest('ul').children();
  const i = lis.index(li);
  lis.removeClass('active');
  li.addClass('active');
  const articles = $(this).closest('.info-page').find('article');
  $(articles.get(i))[0].scrollIntoView();
});

function setupPageSectionObserver() {
  const observer = new IntersectionObserver(function(entries) {
    const target = entries[0].target;
    if (entries[0].isIntersecting) {
      const i = $(target).closest('.content').children().index(target);
      const nav_links = $(target).closest('.info-page').find('.sidebar ul')
      const active_link = nav_links.find('.active')
      const new_link = nav_links.children().get(i);
      active_link.removeClass('active');
      $(new_link).addClass('active');
    }
  }, { threshold: [0.5] });

  $('.info-page article').each(function() {
    observer.observe(this);
  });
}

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