window.onpopstate = function () {
    app.hideAllModals();

    if (document.location.pathname.includes('addEntry') || document.location.pathname.includes('editEntry') ) {
        app.IsEditMode(true);
    }
    else
        app.IsEditMode(false);

    if (document.location.pathname.includes('editEntry')) {
        let url = new URL(document.location);
        let entry_id = url.searchParams.get("id");

        if (entry_id) {
            let entry = app.getEntryById(entry_id);

            app.CurrentEntry(entry);
        }
    }

};