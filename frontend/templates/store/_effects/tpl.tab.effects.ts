/* ----- {{copyright}} --- */
// Angular
import { Injectable } from '@angular/core';
// RxJS
import { of } from 'rxjs';
import { mergeMap, map, catchError, tap } from 'rxjs/operators';
// NGRX
import { Effect, Actions, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
// CRUD
import { QueryResultsModel } from '../../../../../core/_base/crud';
// Services
import { %class%Service } from '../_services/{{selector}}.tab.services';
// State
import { AppState } from '../../../../../core/reducers';
// Actions
import {
    {{class}}ActionTypes,
    {{class}}PageRequested,
    {{class}}PageLoaded,
    Many{{class}}Deleted,
    One{{class}}Deleted,
    {{class}}PageToggleLoading,
    {{class}}Updated,
    {{class}}Created,
    {{class}}OnServerCreated
} from '../_actions/{{selector}}.tab.actions';

@Injectable()
export class {{class}}Effects {
    // showLoadingDistpatcher = new ProcutSpecificationsPageToggleLoading({ isLoading: true });
    hideLoadingDistpatcher = new {{class}}PageToggleLoading({ isLoading: false });

    @Effect()
    load{{class}}Page$ = this.actions$
        .pipe(
            ofType<{{class}}PageRequested>({{class}}ActionTypes.{{class}}PageRequested),
            mergeMap(( { payload } ) => this.{{class}}Service.find{{class}}(payload.page, payload.{{class}}Id)),
            map((result: QueryResultsModel) => {
                return new {{class}}PageLoaded({
                    results: result.results,
                    totalCount: result.totalCount
                });
            }),
        );

    @Effect()
    delete{{class}}$ = this.actions$
        .pipe(
            ofType<One{{class}}Deleted>({{class}}ActionTypes.One{{class}}Deleted),
            mergeMap(( { payload } ) => {
                    this.store.dispatch(new {{class}}PageToggleLoading({ isLoading: true }));
                    return this.{{class}}Service.delete{{class}}(payload.id);
                }
            ),
            map(() => {
                return this.hideLoadingDistpatcher;
            }),
        );

    @Effect()
    delete{{class}}Many$ = this.actions$
        .pipe(
            ofType<Many{{class}}Deleted>({{class}}ActionTypes.Many{{class}}Deleted),
            mergeMap(( { payload } ) => {
                    this.store.dispatch(new {{class}}PageToggleLoading({ isLoading: true }));
                    return this.{{class}}Service.deleteMany{{class}}(payload.ids);
                }
            ),
            map(() => {
                return this.hideLoadingDistpatcher;
            }),
        );

    @Effect()
    update{{class}}$ = this.actions$
        .pipe(
            ofType<{{class}}Updated>({{class}}ActionTypes.{{class}}Updated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(new {{class}}PageToggleLoading({ isLoading: true }));
                return this.{{class}}Service.update{{class}}(payload.{{class}});
            }),
            map(() => {
                return this.hideLoadingDistpatcher;
            }),
        );

    @Effect()
    create{{class}}$ = this.actions$
        .pipe(
            ofType<{{class}}OnServerCreated>({{class}}ActionTypes.{{class}}OnServerCreated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(new {{class}}PageToggleLoading({ isLoading: true }));
                return this.{{class}}Service.create{{class}}(payload.{{class}}).pipe(
                    tap((res: any) => {
                        this.store.dispatch(new {{class}}Created({ {{class}}: res }));
                    })
                );
            }),
            map(() => {
                return this.hideLoadingDistpatcher;
            }),
        );

    constructor(private actions$: Actions, private {{class}}Service: {{class}}Service, private store: Store<AppState>) { }
}
