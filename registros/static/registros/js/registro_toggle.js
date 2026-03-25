// projects/registros/static/registros/js/registro_toggle.js
(function ($) {
  $(function () {
    const $role = $('#id_role');

    // Filas de los campos extra (Django admin genera <div class="form-row field-<nombre>">)
    const $rows = $('.field-edad, .field-escolaridad, .field-numero_empleado');

    function toggleLibrarianExtras() {
      const isLibrarian = $role.val() === 'librarian';
      $rows.toggle(isLibrarian);

      if (!isLibrarian) {
        $('#id_edad').val('');
        $('#id_escolaridad').val('');
        $('#id_numero_empleado').val('');
      }
    }

    toggleLibrarianExtras();
    $role.on('change', toggleLibrarianExtras);
  });
})(django.jQuery);
