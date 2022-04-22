// Angular
import { Injectable } from '@angular/core';
// NGRX
import { Actions, Effect, ofType } from '@ngrx/effects';
import { Action, select, Store } from '@ngrx/store';
// RxJS
import { defer, forkJoin, Observable, of } from 'rxjs';
import { filter, map, mergeMap, tap, withLatestFrom } from 'rxjs/operators';
// State
import { AppState } from '../../../core/reducers';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../_base/crud';
// Actions
import {
    AllRolesLoaded,
    AllRolesRequested,
    RoleActionTypes,
    RoleCreated,
    RoleDeleted,
    RoleOnServerCreated,
    RolesActionToggleLoading,
    RolesPageLoaded,
    RolesPageRequested,
    RolesPageToggleLoading,
    RoleUpdated,
} from '../_actions/role.actions';
// Selectors
import { allRolesLoaded } from '../_selectors/role.selectors';
// Services
import { AuthService } from '../_services';

@Injectable()
export class RoleEffects {
    showPageLoadingDistpatcher = new RolesPageToggleLoading({ isLoading: true });
    hidePageLoadingDistpatcher = new RolesPageToggleLoading({ isLoading: false });

    showActionLoadingDistpatcher = new RolesActionToggleLoading({ isLoading: true });
    hideActionLoadingDistpatcher = new RolesActionToggleLoading({ isLoading: false });

    /*
    @Effect()
    loadAllRoles$ = this.actions$
        .pipe(
            ofType<AllRolesRequested>(RoleActionTypes.AllRolesRequested),
            withLatestFrom(this.store.pipe(select(allRolesLoaded))),
            filter(([action, isAllRolesLoaded]) => !isAllRolesLoaded),
            mergeMap(() => this.auth.getAllRoles()),
            map(roles => {
                return new AllRolesLoaded({roles});
            })
          );
    */

    @Effect()
    loadRolesPage$ = this.actions$
        .pipe(
            ofType<RolesPageRequested>(RoleActionTypes.RolesPageRequested),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showPageLoadingDistpatcher);
                const requestToServer = this.auth.findRoles(payload.page);
                const lastQuery = of(payload.page);
                return forkJoin(requestToServer, lastQuery);
            }),
            map(response => {
                const result: QueryResultsModel = response[0];
                const lastQuery: QueryParamsModel = response[1];
                this.store.dispatch(this.hidePageLoadingDistpatcher);

                return new RolesPageLoaded({
                    roles: result.items,
                    totalCount: result.totalCount,
                    page: lastQuery,
                });
            }),
        );

    @Effect()
    deleteRole$ = this.actions$
        .pipe(
            ofType<RoleDeleted>(RoleActionTypes.RoleDeleted),
            mergeMap(( { payload } ) => {
                    this.store.dispatch(this.showActionLoadingDistpatcher);
                    return this.auth.deleteRole(payload.id);
                },
            ),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    updateRole$ = this.actions$
        .pipe(
            ofType<RoleUpdated>(RoleActionTypes.RoleUpdated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showActionLoadingDistpatcher);
                return this.auth.updateRole(payload.role);
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    createRole$ = this.actions$
        .pipe(
            ofType<RoleOnServerCreated>(RoleActionTypes.RoleOnServerCreated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showActionLoadingDistpatcher);
                return this.auth.createRole(payload.role).pipe(
                    tap(res => {
                        this.store.dispatch(new RoleCreated({ role: res }));
                    }),
                );
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    init$: Observable<Action> = defer(() => {
        return of(new AllRolesRequested());
    });

    constructor(private actions$: Actions, private auth: AuthService, private store: Store<AppState>) { }
}
