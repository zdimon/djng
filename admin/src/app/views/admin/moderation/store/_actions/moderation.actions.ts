/* -----  --- */
// NGRX
import { Action } from '@ngrx/store';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { ModerationModel } from '../_models/moderation.model';
import { Update } from '@ngrx/entity';

export enum ModerationActionTypes {
    ModerationOnServerCreated = '[Edit Moderation Component] Moderation On Server Created',
    ModerationCreated = '[Edit Moderation Component] Moderation Created',
    ModerationUpdated = '[Edit Moderation Component] Moderation Updated',
    ModerationsStatusUpdated = '[Moderation List Page] Moderation Status Updated',
    OneModerationDeleted = '[Moderation List Page] One Video Deleted',
    ManyModerationsDeleted = '[Moderation List Page] Many Selected Moderations Deleted',
    ModerationsPageRequested = '[Moderation List Page] Moderations Page Requested',
    ModerationsPageLoaded = '[Moderation API] Moderations Page Loaded',
    ModerationsPageCancelled = '[Moderation API] Moderations Page Cancelled',
    ModerationsPageToggleLoading = '[Moderation] Moderations Page Toggle Loading',
    ModerationsActionToggleLoading = '[Moderation] Moderations Action Toggle Loading'
}

export class ModerationOnServerCreated implements Action {
    readonly type = ModerationActionTypes.ModerationOnServerCreated;
    constructor(public payload: { moderation: ModerationModel }) { }
}

export class ModerationCreated implements Action {
    readonly type = ModerationActionTypes.ModerationCreated;
    constructor(public payload: { moderation: ModerationModel }) { }
}

export class ModerationUpdated implements Action {
    readonly type = ModerationActionTypes.ModerationUpdated;
    constructor(public payload: {
        partialModeration: Update<ModerationModel>, // For State update
        results: ModerationModel // For Server update (through service)
    }) { }
}

export class ModerationsStatusUpdated implements Action {
    readonly type = ModerationActionTypes.ModerationsStatusUpdated;
    constructor(public payload: {
        results: ModerationModel[],
        status: number
    }) { }
}

export class OneModerationDeleted implements Action {
    readonly type = ModerationActionTypes.OneModerationDeleted;
    constructor(public payload: { id: number }) {}
}

export class ManyModerationsDeleted implements Action {
    readonly type = ModerationActionTypes.ManyModerationsDeleted;
    constructor(public payload: { ids: number[] }) {}
}

export class ModerationsPageRequested implements Action {
    readonly type = ModerationActionTypes.ModerationsPageRequested;
    constructor(public payload: { page: QueryParamsModel }) { }
}

export class ModerationsPageLoaded implements Action {
    readonly type = ModerationActionTypes.ModerationsPageLoaded;
    constructor(public payload: { results: ModerationModel[], totalCount: number, page: QueryParamsModel }) { }
}

export class ModerationsPageCancelled implements Action {
    readonly type = ModerationActionTypes.ModerationsPageCancelled;
}

export class ModerationsPageToggleLoading implements Action {
    readonly type = ModerationActionTypes.ModerationsPageToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export class ModerationsActionToggleLoading implements Action {
    readonly type = ModerationActionTypes.ModerationsActionToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export type ModerationActions = ModerationOnServerCreated
| ModerationCreated
| ModerationUpdated
| ModerationsStatusUpdated
| OneModerationDeleted
| ManyModerationsDeleted
| ModerationsPageRequested
| ModerationsPageLoaded
| ModerationsPageCancelled
| ModerationsPageToggleLoading
| ModerationsActionToggleLoading;
