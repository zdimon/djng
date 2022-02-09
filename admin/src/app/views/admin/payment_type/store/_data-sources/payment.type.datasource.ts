/* -----  --- */
import { selectPaymentTypesInitWaitingMessage } from '../_selectors/payment.type.selectors';
// RxJS
import { delay, distinctUntilChanged } from 'rxjs/operators';
// CRUD
import { DjangoQueryResultsModel, QueryResultsModel, BaseDataSource } from '@core/_base/crud';
// State
import { Store, select } from '@ngrx/store';
import { AppState } from '../../../../../core/reducers';
// Selectors
import { selectPaymentTypesInStore, selectPaymentTypesPageLoading } from '../_selectors/payment.type.selectors';

export class PaymentTypesDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();
        this.loading$ = this.store.pipe(
            select(selectPaymentTypesPageLoading)
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectPaymentTypesInitWaitingMessage)
        );

        this.store.pipe(
            select(selectPaymentTypesInStore)
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}
