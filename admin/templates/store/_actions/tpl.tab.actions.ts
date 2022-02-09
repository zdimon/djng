/* ----- {{copyright}} --- */
// NGRX
// CRUD
import { Update } from '@ngrx/entity';
import { Action } from '@ngrx/store';
import { QueryParamsModel } from '../../../../../core/_base/crud';
// Models
import { %class%Model } from '../_models/{{selector}}.tab.model';

export enum {{class}}ActionTypes {
    {{class}}OnServerCreated = '[Edit {{class}} Dialog] {{class}} On Server Created',
    {{class}}Created = '[Edit {{class}} Dialog] {{class}} Created',
    {{class}}Updated = '[Edit {{class}} Dialog] {{class}} Updated',
    One{{class}}Deleted = '[{{class}} List Page]  One {{class}} Deleted',
    Many{{class}}Deleted = '[{{class}} List Page] Many {{class}} Deleted',
    {{class}}PageRequested = '[{{class}} List Page] Page Requested',
    {{class}}PageLoaded = '[{{class}} API] Page Loaded',
    {{class}}PageCancelled = '[{{class}} API] Page Cancelled',
    {{class}}PageToggleLoading = '[{{class}}] {{class}} Page Toggle Loading'
}

export class {{class}}OnServerCreated implements Action {
    readonly type = {{class}}ActionTypes.{{class}}OnServerCreated;
    constructor(public payload: { {{class}}: {{class}}Model }) { }
}

export class {{class}}Created implements Action {
    readonly type = {{class}}ActionTypes.{{class}}Created;
    constructor(public payload: { {{class}}: {{class}}Model }) { }
}

export class {{class}}Updated implements Action {
    readonly type = {{class}}ActionTypes.{{class}}Updated;
    constructor(public payload: {
        partial{{class}}: Update<{{class}}Model>, // For State update
        {{class}}: {{class}}Model,  // For Server update (through service)
    }) { }
}

export class One{{class}}Deleted implements Action {
    readonly type = {{class}}ActionTypes.One{{class}}Deleted;
    constructor(public payload: { id: number }) {}
}

export class Many{{class}}Deleted implements Action {
    readonly type = {{class}}ActionTypes.Many{{class}}Deleted;
    constructor(public payload: { ids: number[] }) {}
}

export class {{class}}PageRequested implements Action {
    readonly type = {{class}}ActionTypes.{{class}}PageRequested;
    constructor(public payload: { page: QueryParamsModel, {{class}}Id: number }) { }
}

export class {{class}}PageLoaded implements Action {
    readonly type = {{class}}ActionTypes.{{class}}PageLoaded;
    constructor(public payload: { results: {{class}}Model[], totalCount: number }) { }
}

export class {{class}}PageCancelled implements Action {
    readonly type = {{class}}ActionTypes.{{class}}PageCancelled;
}

export class {{class}}PageToggleLoading implements Action {
    readonly type = {{class}}ActionTypes.{{class}}PageToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export type {{class}}Actions = {{class}}OnServerCreated
| {{class}}Created
| {{class}}Updated
| One{{class}}Deleted
| Many{{class}}Deleted
| {{class}}PageRequested
| {{class}}PageLoaded
| {{class}}PageCancelled
| {{class}}PageToggleLoading;

