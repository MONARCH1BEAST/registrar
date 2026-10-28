(function () {
  "use strict";

  var search = document.getElementById("student-search");
  var filter = document.getElementById("status-filter");
  var rows = document.querySelectorAll(".student-row");
  var count = document.getElementById("result-count");
  var empty = document.getElementById("filter-empty");
  var deleteModal = document.querySelector("[data-delete-modal]");
  var deleteDialog = deleteModal ? deleteModal.querySelector('[role="dialog"]') : null;
  var deleteCancel = deleteModal ? deleteModal.querySelector("[data-delete-cancel]") : null;
  var deleteConfirm = deleteModal ? deleteModal.querySelector("[data-delete-confirm]") : null;
  var deleteStudentName = deleteModal ? deleteModal.querySelector("[data-delete-student-name]") : null;
  var deleteStudentRoll = deleteModal ? deleteModal.querySelector("[data-delete-student-roll]") : null;
  var appShell = document.querySelector(".app-shell");
  var activeDeleteForm = null;
  var activeDeleteTrigger = null;
  var previousFocus = null;

  function updateRows() {
    if (!rows.length) return;
    var text = search ? search.value.trim().toLowerCase() : "";
    var status = filter ? filter.value : "all";
    var visible = 0;
    rows.forEach(function (row) {
      var matchesText = !text || row.getAttribute("data-search").indexOf(text) !== -1;
      var matchesStatus = status === "all" || row.getAttribute("data-status") === status;
      row.hidden = !(matchesText && matchesStatus);
      if (!row.hidden) visible += 1;
    });
    if (count) count.textContent = visible + (visible === 1 ? " record" : " records");
    if (empty) empty.hidden = visible !== 0;
  }

  if (search) search.addEventListener("input", updateRows);
  if (filter) filter.addEventListener("change", updateRows);
  document.querySelectorAll("[data-clear-filters]").forEach(function (button) {
    button.addEventListener("click", function () {
      if (search) search.value = "";
      if (filter) filter.value = "all";
      updateRows();
      if (search) search.focus();
    });
  });
  document.querySelectorAll("form[data-loading]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (form.hasAttribute("data-delete-form")) {
        if (form.dataset.submitting === "true") {
          event.preventDefault();
          return;
        }
        if (form.dataset.confirmed !== "true") {
          event.preventDefault();
          openDeleteModal(form, event.submitter || form.querySelector('[type="submit"]'));
          return;
        }
        form.dataset.submitting = "true";
      }
      var submit = event.submitter || form.querySelector('[type="submit"]');
      form.setAttribute("aria-busy", "true");
      if (submit) {
        submit.disabled = true;
        submit.textContent = form.getAttribute("data-loading");
      }
    });
  });

  function openDeleteModal(form, trigger) {
    if (!deleteModal || !deleteDialog || !deleteCancel) return;
    activeDeleteForm = form;
    activeDeleteTrigger = trigger;
    previousFocus = document.activeElement;
    deleteStudentName.textContent = form.dataset.studentName;
    deleteStudentRoll.textContent = form.dataset.studentRoll;
    deleteModal.hidden = false;
    document.body.classList.add("modal-open");
    if (appShell) appShell.inert = true;
    deleteCancel.focus();
  }

  function closeDeleteModal(restoreFocus) {
    if (!deleteModal) return;
    deleteModal.hidden = true;
    document.body.classList.remove("modal-open");
    if (appShell) appShell.inert = false;
    if (restoreFocus && previousFocus && previousFocus.isConnected) previousFocus.focus();
    activeDeleteForm = null;
    activeDeleteTrigger = null;
    previousFocus = null;
  }

  if (deleteCancel) {
    deleteCancel.addEventListener("click", function () {
      closeDeleteModal(true);
    });
  }
  if (deleteModal) {
    deleteModal.addEventListener("click", function (event) {
      if (event.target === deleteModal) closeDeleteModal(true);
    });
  }
  if (deleteConfirm) {
    deleteConfirm.addEventListener("click", function () {
      if (!activeDeleteForm || activeDeleteForm.dataset.submitting === "true") return;
      var form = activeDeleteForm;
      var trigger = activeDeleteTrigger;
      form.dataset.confirmed = "true";
      closeDeleteModal(false);
      form.requestSubmit(trigger || undefined);
    });
  }
  document.addEventListener("keydown", function (event) {
    if (!deleteModal || deleteModal.hidden) return;
    if (event.key === "Escape") {
      event.preventDefault();
      closeDeleteModal(true);
      return;
    }
    if (event.key !== "Tab" || !deleteDialog) return;
    var focusable = deleteDialog.querySelectorAll('button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])');
    if (!focusable.length) {
      event.preventDefault();
      deleteDialog.focus();
      return;
    }
    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
}());
