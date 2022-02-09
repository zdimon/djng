/* -----  --- */
// Context
//export { ECommerceDataContext } from './_server/_e-commerce.data-context';

// Models and Consts
export { PaymentModel } from './_models/payment.model';


// DataSources
export { PaymentsDataSource } from './_data-sources/payment.datasource';

// Actions
// Customer Actions =>

// Video actions =>
export {
    PaymentActionTypes,
    PaymentActions,
    PaymentOnServerCreated,
    PaymentCreated,
    PaymentUpdated,
    PaymentsStatusUpdated,
    OnePaymentDeleted,
    ManyPaymentsDeleted,
    PaymentsPageRequested,
    PaymentsPageLoaded,
    PaymentsPageCancelled,
    PaymentsPageToggleLoading,
    PaymentsActionToggleLoading
} from './_actions/payment.actions';


// Effects

export { PaymentEffects } from './_effects/payment.effects';

// Reducers
export { paymentReducer } from './_reducers/payment.reducers';


// Product selectors
export {
    selectPaymentById,
    selectPaymentsInStore,
    selectPaymentsPageLoading,
    selectPaymentsPageLastQuery,
    selectLastCreatedPaymentId,
    selectHasPaymentsInStore,
    selectPaymentsActionLoading,
    selectPaymentsInitWaitingMessage
} from './_selectors/payment.selectors';

// Services

export { PaymentService } from './_services/';
export {HttpUtilsService} from './_services/payment.utils';

