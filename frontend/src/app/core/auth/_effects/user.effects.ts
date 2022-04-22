// Angular
import { Injectable } from '@angular/core';
// NGRX
import { Actions, Effect, ofType } from '@ngrx/effects';
import { Action, select, Store } from '@ngrx/store';
import { defer, forkJoin, Observable, of } from 'rxjs';
// RxJS
import { map, mergeMap, tap } from 'rxjs/operators';
// Services
import { AuthService } from '../../../core/auth/_services';
// State
import { AppState } from '../../../core/reducers';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../_base/crud';

import {
    UserActionTypes,
    UserCreated,
    UserDeleted,
    UserOnServerCreated,
    UsersActionToggleLoading,
    UsersPageLoaded,
    UsersPageRequested,
    UsersPageToggleLoading,
    UserUpdated,
} from '../_actions/user.actions';

@Injectable()
export class UserEffects {
    showPageLoadingDistpatcher = new UsersPageToggleLoading({ isLoading: true });
    hidePageLoadingDistpatcher = new UsersPageToggleLoading({ isLoading: false });

    showActionLoadingDistpatcher = new UsersActionToggleLoading({ isLoading: true });
    hideActionLoadingDistpatcher = new UsersActionToggleLoading({ isLoading: false });

    @Effect()
    loadUsersPage$ = this.actions$
        .pipe(
            ofType<UsersPageRequested>(UserActionTypes.UsersPageRequested),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showPageLoadingDistpatcher);
                const requestToServer = this.auth.findUsers(payload.page);
                const lastQuery = of(payload.page);
                return forkJoin(requestToServer, lastQuery);
            }),
            map(response => {
                const result: QueryResultsModel = response[0];
                const lastQuery: QueryParamsModel = response[1];
                return new UsersPageLoaded({
                    users: result.items,
                    totalCount: result.totalCount,
                    page: lastQuery,
                });
            }),
        );

    @Effect()
    deleteUser$ = this.actions$
        .pipe(
            ofType<UserDeleted>(UserActionTypes.UserDeleted),
            mergeMap(( { payload } ) => {
                    this.store.dispatch(this.showActionLoadingDistpatcher);
                    return this.auth.deleteUser(payload.id);
                },
            ),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    updateUser$ = this.actions$
        .pipe(
            ofType<UserUpdated>(UserActionTypes.UserUpdated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showActionLoadingDistpatcher);
                return this.auth.updateUser(payload.user);
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    createUser$ = this.actions$
        .pipe(
            ofType<UserOnServerCreated>(UserActionTypes.UserOnServerCreated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showActionLoadingDistpatcher);
                return this.auth.createUser(payload.user).pipe(
                    tap(res => {
                        this.store.dispatch(new UserCreated({ user: res }));
                    }),
                );
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    constructor(private actions$: Actions, private auth: AuthService, private store: Store<AppState>) { }
}
