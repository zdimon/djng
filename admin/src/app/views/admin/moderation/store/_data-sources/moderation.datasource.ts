/* -----  --- */
import { selectModerationsInitWaitingMessage } from '../_selectors/moderation.selectors';
// RxJS
import { delay, distinctUntilChanged } from 'rxjs/operators';
// CRUD
import { DjangoQueryResultsModel, QueryResultsModel, BaseDataSource } from '@core/_base/crud';
// State
import { Store, select } from '@ngrx/store';
import { AppState } from '../../../../../core/reducers';
// Selectors
import { selectModerationsInStore, selectModerationsPageLoading } from '../_selectors/moderation.selectors';

export class ModerationsDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();
        this.loading$ = this.store.pipe(
            select(selectModerationsPageLoading)
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectModerationsInitWaitingMessage)
        );

        this.store.pipe(
            select(selectModerationsInStore)
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}
