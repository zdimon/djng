// RxJS
// NGRX
import { select, Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, debounceTime, delay, distinctUntilChanged, finalize, tap } from 'rxjs/operators';
// State
import { AppState } from '../../../core/reducers';
// CRUD
import { BaseDataSource, QueryResultsModel } from '../../_base/crud';
// Selectirs
import { selectQueryResult, selectRolesPageLoading, selectRolesShowInitWaitingMessage } from '../_selectors/role.selectors';

export class RolesDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();

        this.loading$ = this.store.pipe(
            select(selectRolesPageLoading),
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectRolesShowInitWaitingMessage),
        );

        this.store.pipe(
            select(selectQueryResult),
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });

    }
}
