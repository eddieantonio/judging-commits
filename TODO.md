 - [ ] Tokenize every commit message, by project. Pickle.
 - [x] Download data from Travis-CI, GHTorrent
 - [ ] ~~For each project: train model on all projects other than
        current.~~ Do cross-folds validation.
 - [ ] Validate the model against each project -- one-way ANOVA should
       say it's not different
 - [ ] If everything checks out -- assumption is that no one project's
       model is sufficiently different, then we're in business! 
