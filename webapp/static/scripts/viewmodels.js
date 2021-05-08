'strict';
var host = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');

//Main Application ViewModel
function App() {
    let _self = this;
    this.Book = ko.observable(new BookViewModel());
    this.IsEditMode = ko.observable(false);
    this.Processing = ko.observable(false);
    this.CurrentEntry = ko.observable();
    this.Outcome = ko.observable(new OutcomeViewModel({ action: _self.hideAllModals }));
    this.EditActionLabel = ko.observable('Post');
}

App.prototype.getBook = function () {
    let _self = this;
    _self.Processing(true);
    fetch(host + '/book')
        .then(function (response) {
            if (response.ok)
                return response.json();
            else
                app.Processing(false);

        }).then(function (response) {
            if (response.status === false)
                console.log(response.message);
            else if (response.data && response.data.book) {
                const book = response.data.book;
                _self.Book(new BookViewModel(book));
            }
            _self.Processing(false);
        });
};

App.prototype.addEntry = function () {
    let _self = this;

    _self.CurrentEntry(new BookEntryViewModel({ is_new: true }));
    _self.EditActionLabel('Post');
    _self.showAddModal();
    bsCustomFileInput.init('.custom-file-input');
};

App.prototype.getEntryById = function (entry_id) {
    let _self = this;

    let entry = _self.Book().BookEntries().filter(entry => entry.Id().toString() === entry_id.toString());

    if (entry)
        return entry[0];
    else
        return new BookEntryViewModel();
};

App.prototype.showDeleteModal = function () {
    $('#deleteModal').modal('show');
};

App.prototype.showEditModal = function () {
    $('#editModal').modal('show');
};

App.prototype.showKeyModal = function () {
    $('#keyModal').modal('show');
};

App.prototype.showOutcomeModal = function () {
    app.hideAllModals();
    $('#outcomeModal').modal('show');
};

App.prototype.hideAllModals = function () {
    $('.modal').modal('hide');
};

App.prototype.showAddModal = function () {
    $('#addModal').modal('show');
};

function BookViewModel(model) {
    let _self = this;

    this.BookEntries = ko.observableArray([]);

    if (model)
        _self.SetFromModel(model);
}

BookViewModel.prototype.SetFromModel = function (model) {
    let _self = this;

    if (model.book_entries) {
        model.book_entries.forEach(book_entry_model => {
            _self.BookEntries.push(new BookEntryViewModel(book_entry_model));
        });
    }
};

BookViewModel.prototype.ToModel = function () {
    let _self = this;

    let model = {
        book_entries: []
    };

    _self.BookEntries().forEach(book_entry => {
        model.book_entries.push(book_entry.ToModel());
    });

    return model;
};

function BookEntryViewModel(model) {
    let _self = this;

    this.Id = ko.observable('');
    this.Author = ko.observable('');
    this.Message = ko.observable('');
    this.SavedVideo = ko.observable();
    this.SavedImage = ko.observable();
    this.NewVideo = ko.observable();
    this.NewImage = ko.observable();
    this.IsNew = ko.observable(false);

    if (model)
        _self.SetFromModel(model);
}

BookEntryViewModel.prototype.SetFromModel = function (model) {
    let _self = this;

    if (model.id)
        _self.Id(model.id);

    if (model.author)
        _self.Author(model.author);

    if (model.message)
        _self.Message(model.message);

    if (model.video_path)
        _self.SavedVideo(model.video_path);

    if (model.image_path)
        _self.SavedImage(model.image_path);

    if (model.is_new)
        _self.IsNew(model.is_new);
};

BookEntryViewModel.prototype.ToModel = function () {
    let _self = this;

    let model = {
        id: _self.Id(),
        author: _self.Author(),
        message: _self.Message(),
        video_path: _self.SavedVideo() ? _self.SavedVideo() : '',
        image_path: _self.SavedImage() ? _self.SavedImage() : ''
    };

    return model;
};

BookEntryViewModel.prototype.DeleteVideo = function () {
    let _self = this;

    _self.SavedVideo(null);
};

BookEntryViewModel.prototype.DeleteImage = function () {
    let _self = this;

    _self.SavedImage(null);
};

BookEntryViewModel.prototype.updateBookEntry = function () {
    let _self = this;

    app.hideAllModals();
    app.Processing(true);

    let form = new FormData();

    if(_self.NewVideo())
        form.append("video", _self.NewVideo());

    if (_self.NewImage())
        form.append("image", _self.NewImage());

    form.append("book_entry", JSON.stringify(_self.ToModel()));    

    fetch(host + '/updatebookentry',
        {
            method: 'POST',
            body: form
        })
        .then(function (response) {
            if (response.ok)
                return response.json();
            else {
                app.Processing(false);
                app.Outcome().Message("Sorry, something didn't work :(");
                app.showOutcomeModal();
            }

        }).then(function (response) {

            app.Processing(false);

            if (response.status === false) {
                console.log(response.message);
                app.Outcome().Message(response.message);
                app.showOutcomeModal();
            }
            else
                if (response.data.is_new) {
                    _self.Id(response.data.id);
                    app.Outcome().Message(response.message);
                    app.showOutcomeModal();
                    app.Book().BookEntries.push(_self);
                }
                else {
                    app.Outcome().Message(response.message);
                    app.showOutcomeModal();
                }
        });
};

BookEntryViewModel.prototype.deleteBookEntry = function () {
    let _self = this;

    app.hideAllModals();
    app.Processing(true);

    let data = {
        book_entry_id: _self.Id()
    };

    fetch(host + '/deletebookentry',
        {
            method: 'POST',
            body: JSON.stringify(data)
        })
        .then(function (response) {
            if (response.ok)
                return response.json();
            else {
                app.Processing(false);
                app.Outcome().Message("Sorry, something didn't work :(");
                app.showOutcomeModal();
            }

        }).then(function (response) {
            app.Processing(false);

            if (response.status === false) {
                console.log(response.message);
                app.Outcome().Message(response.message);
                app.showOutcomeModal();
            }
                
            else {
                app.Book().BookEntries.remove(_self);
                app.Outcome().Message(response.message);
                app.showOutcomeModal();
            }
        });
};

BookEntryViewModel.prototype.startDeleteProcess = function () {
    let _self = this;

    app.CurrentEntry(_self);
    app.hideAllModals();
    app.showDeleteModal();
};

BookEntryViewModel.prototype.startEditProcess = function () {
    let _self = this;

    app.CurrentEntry(_self);
    app.EditActionLabel('Save');

    bsCustomFileInput.init('.custom-file-input');
    app.showAddModal();

};

function OutcomeViewModel(model) {
    let _self = this;

    this.Message = ko.observable();
    this.Action = ko.observable();

    if (model)
        _self.SetFromModel(model);
}

OutcomeViewModel.prototype.SetFromModel = function (model) {
    let _self = this;

    if (model.message) 
        _self.Message(model.message);

    if (model.action)
        _self.Action(model.action);
};