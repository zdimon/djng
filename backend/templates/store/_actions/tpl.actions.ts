/* ----- {{copyright}} --- */
// NGRX
import { Action } from '@ngrx/store';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { {{upname}}Model } from '../_models/{{fileprefix}}.model';
import { Update } from '@ngrx/entity';

export enum {{upname}}ActionTypes {
    {{upname}}OnServerCreated = '[Edit {{upname}} Component] {{upname}} On Server Created',
    {{upname}}Created = '[Edit {{upname}} Component] {{upname}} Created',
    {{upname}}Updated = '[Edit {{upname}} Component] {{upname}} Updated',
    {{upname}}sStatusUpdated = '[{{upname}} List Page] {{upname}} Status Updated',
    One{{upname}}Deleted = '[{{upname}} List Page] One Video Deleted',
    Many{{upname}}sDeleted = '[{{upname}} List Page] Many Selected {{upname}}s Deleted',
    {{upname}}sPageRequested = '[{{upname}} List Page] {{upname}}s Page Requested',
    {{upname}}sPageLoaded = '[{{upname}} API] {{upname}}s Page Loaded',
    {{upname}}sPageCancelled = '[{{upname}} API] {{upname}}s Page Cancelled',
    {{upname}}sPageToggleLoading = '[{{upname}}] {{upname}}s Page Toggle Loading',
    {{upname}}sActionToggleLoading = '[{{upname}}] {{upname}}s Action Toggle Loading'
}

export class {{upname}}OnServerCreated implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}OnServerCreated;
    constructor(public payload: { {{camelName}}: {{upname}}Model }) { }
}

export class {{upname}}Created implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}Created;
    constructor(public payload: { {{camelName}}: {{upname}}Model }) { }
}

export class {{upname}}Updated implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}Updated;
    constructor(public payload: {
        partial{{upname}}: Update<{{upname}}Model>, // For State update
        results: {{upname}}Model // For Server update (through service)
    }) { }
}

export class {{upname}}sStatusUpdated implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}sStatusUpdated;
    constructor(public payload: {
        results: {{upname}}Model[],
        status: number
    }) { }
}

export class One{{upname}}Deleted implements Action {
    readonly type = {{upname}}ActionTypes.One{{upname}}Deleted;
    constructor(public payload: { id: number }) {}
}

export class Many{{upname}}sDeleted implements Action {
    readonly type = {{upname}}ActionTypes.Many{{upname}}sDeleted;
    constructor(public payload: { ids: number[] }) {}
}

export class {{upname}}sPageRequested implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}sPageRequested;
    constructor(public payload: { page: QueryParamsModel }) { }
}

export class {{upname}}sPageLoaded implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}sPageLoaded;
    constructor(public payload: { results: {{upname}}Model[], totalCount: number, page: QueryParamsModel }) { }
}

export class {{upname}}sPageCancelled implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}sPageCancelled;
}

export class {{upname}}sPageToggleLoading implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}sPageToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export class {{upname}}sActionToggleLoading implements Action {
    readonly type = {{upname}}ActionTypes.{{upname}}sActionToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export type {{upname}}Actions = {{upname}}OnServerCreated
| {{upname}}Created
| {{upname}}Updated
| {{upname}}sStatusUpdated
| One{{upname}}Deleted
| Many{{upname}}sDeleted
| {{upname}}sPageRequested
| {{upname}}sPageLoaded
| {{upname}}sPageCancelled
| {{upname}}sPageToggleLoading
| {{upname}}sActionToggleLoading;
