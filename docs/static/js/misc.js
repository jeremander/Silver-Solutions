// switch between subpages by clicking on links
$('.subpage-link').click(function () {
  const li = $(this).closest('li');
  const lis = $(this).closest('ul').children();
  const i = lis.index(li);
  lis.removeClass('active');
  li.addClass('active');
  const articles = $(this).closest('.left-sidebar').find('article');
  articles.removeClass('visible');
  $(articles.get(i)).addClass('visible');
});