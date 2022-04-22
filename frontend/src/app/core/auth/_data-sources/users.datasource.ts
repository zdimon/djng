// RxJS
// NGRX
import { select, Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, debounceTime, delay, distinctUntilChanged, finalize, tap } from 'rxjs/operators';
// State
import { AppState } from '../../../core/reducers';
// CRUD
import { BaseDataSource, QueryResultsModel } from '../../_base/crud';
import { selectUsersInStore, selectUsersPageLoading, selectUsersShowInitWaitingMessage } from '../_selectors/user.selectors';

export class UsersDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();

        this.loading$ = this.store.pipe(
            select(selectUsersPageLoading),
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectUsersShowInitWaitingMessage),
        );

        this.store.pipe(
            select(selectUsersInStore),
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}
