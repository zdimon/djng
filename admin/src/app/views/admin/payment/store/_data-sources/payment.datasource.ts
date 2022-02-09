/* -----  --- */
import { selectPaymentsInitWaitingMessage } from '../_selectors/payment.selectors';
// RxJS
import { delay, distinctUntilChanged } from 'rxjs/operators';
// CRUD
import { DjangoQueryResultsModel, QueryResultsModel, BaseDataSource } from '@core/_base/crud';
// State
import { Store, select } from '@ngrx/store';
import { AppState } from '../../../../../core/reducers';
// Selectors
import { selectPaymentsInStore, selectPaymentsPageLoading } from '../_selectors/payment.selectors';

export class PaymentsDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();
        this.loading$ = this.store.pipe(
            select(selectPaymentsPageLoading)
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectPaymentsInitWaitingMessage)
        );

        this.store.pipe(
            select(selectPaymentsInStore)
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}
