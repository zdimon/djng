/* ----- {{copyright}} --- */
// Context
//export { ECommerceDataContext } from './_server/_e-commerce.data-context';

// Models and Consts
export { {{upname}}Model } from './_models/{{fileprefix}}.model';


// DataSources
export { {{upname}}sDataSource } from './_data-sources/{{fileprefix}}.datasource';

// Actions
// Customer Actions =>

// Video actions =>
export {
    {{upname}}ActionTypes,
    {{upname}}Actions,
    {{upname}}OnServerCreated,
    {{upname}}Created,
    {{upname}}Updated,
    {{upname}}sStatusUpdated,
    One{{upname}}Deleted,
    Many{{upname}}sDeleted,
    {{upname}}sPageRequested,
    {{upname}}sPageLoaded,
    {{upname}}sPageCancelled,
    {{upname}}sPageToggleLoading,
    {{upname}}sActionToggleLoading
} from './_actions/{{fileprefix}}.actions';


// Effects

export { {{upname}}Effects } from './_effects/{{fileprefix}}.effects';

// Reducers
export { {{ camelName }}Reducer } from './_reducers/{{fileprefix}}.reducers';


// Product selectors
export {
    select{{upname}}ById,
    select{{upname}}sInStore,
    select{{upname}}sPageLoading,
    select{{upname}}sPageLastQuery,
    selectLastCreated{{upname}}Id,
    selectHas{{upname}}sInStore,
    select{{upname}}sActionLoading,
    select{{upname}}sInitWaitingMessage
} from './_selectors/{{fileprefix}}.selectors';

// Services

export { {{upname}}Service } from './_services/';
export {HttpUtilsService} from './_services/{{fileprefix}}.utils';

