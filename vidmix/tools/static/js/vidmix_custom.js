document.addEventListener('DOMContentLoaded', () => {
  const player = Plyr.setup('.js-player');
});

$(document).ready(function () {
  $('#example').DataTable({
    "ordering": false,
    "scrollY": '27vh',
    "paging": false,
    "bInfo": false,
  });
});