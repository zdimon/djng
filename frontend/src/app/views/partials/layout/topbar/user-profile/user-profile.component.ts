// Angular
import { Component, Input, OnInit } from '@angular/core';
// NGRX
import { select, Store } from '@ngrx/store';
// RxJS
import { Observable } from 'rxjs';
import { currentUser, Logout, User } from '../../../../../core/auth';
// State
import { AppState } from '../../../../../core/reducers';

@Component({
    selector: 'kt-user-profile',
    templateUrl: './user-profile.component.html',
})
export class UserProfileComponent implements OnInit {
    // Public properties
    user$: Observable<User>;

    @Input() avatar = true;
    @Input() greeting = true;
    @Input() badge: boolean;
    @Input() icon: boolean;

    /**
     * Component constructor
     *
     * @param store: Store<AppState>
     */
    constructor(private store: Store<AppState>) {
    }

    /**
     * @ Lifecycle sequences => https://angular.io/guide/lifecycle-hooks
     */

    /**
     * On init
     */
    ngOnInit(): void {
        this.user$ = this.store.pipe(select(currentUser));
    }

    /**
     * Log out
     */
    logout() {
        this.store.dispatch(new Logout());
    }
}
