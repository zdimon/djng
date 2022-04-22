/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */
import { selectUsersInitWaitingMessage } from '../_selectors/user.selectors';
// RxJS
import { delay, distinctUntilChanged } from 'rxjs/operators';
// CRUD
import { DjangoQueryResultsModel, QueryResultsModel, BaseDataSource } from '@core/_base/crud';
// State
import { Store, select } from '@ngrx/store';
import { AppState } from '../../../../../core/reducers';
// Selectors
import { selectUsersInStore, selectUsersPageLoading } from '../_selectors/user.selectors';

export class UsersDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();
        this.loading$ = this.store.pipe(
            select(selectUsersPageLoading)
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectUsersInitWaitingMessage)
        );

        this.store.pipe(
            select(selectUsersInStore)
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}