// NGRX
import { Update } from '@ngrx/entity';
import { Action } from '@ngrx/store';
// CRUD
import { QueryParamsModel } from '../../../_base/crud';
// Models
import { VideoModel } from '../_models/video.model';

export enum VideoActionTypes {
    VideoOnServerCreated = '[Edit Video Component] Video On Server Created',
    VideoCreated = '[Edit Video Component] Video Created',
    VideoUpdated = '[Edit Video Component] Video Updated',
    VideosStatusUpdated = '[Products List Page] Products Status Updated',
    OneVideoDeleted = '[Video List Page] One Video Deleted',
    ManyVideosDeleted = '[Video List Page] Many Selected Videos Deleted',
    VideosPageRequested = '[Videos List Page] Videos Page Requested',
    VideosPageLoaded = '[Videos API] Videos Page Loaded',
    VideosPageCancelled = '[Videos API] Videos Page Cancelled',
    VideosPageToggleLoading = '[Videos] Videos Page Toggle Loading',
    VideosActionToggleLoading = '[Videos] Videos Action Toggle Loading',
}

export class VideoOnServerCreated implements Action {
    readonly type = VideoActionTypes.VideoOnServerCreated;
    constructor(public payload: { video: VideoModel }) { }
}

export class VideoCreated implements Action {
    readonly type = VideoActionTypes.VideoCreated;
    constructor(public payload: { video: VideoModel }) { }
}

export class VideoUpdated implements Action {
    readonly type = VideoActionTypes.VideoUpdated;
    constructor(public payload: {
        partialProduct: Update<VideoModel>, // For State update
        results: VideoModel, // For Server update (through service)
    }) { }
}

export class VideosStatusUpdated implements Action {
    readonly type = VideoActionTypes.VideosStatusUpdated;
    constructor(public payload: {
        results: VideoModel[],
        status: number,
    }) { }
}

export class OneVideoDeleted implements Action {
    readonly type = VideoActionTypes.OneVideoDeleted;
    constructor(public payload: { id: number }) {}
}

export class ManyVideosDeleted implements Action {
    readonly type = VideoActionTypes.ManyVideosDeleted;
    constructor(public payload: { ids: number[] }) {}
}

export class VideosPageRequested implements Action {
    readonly type = VideoActionTypes.VideosPageRequested;
    constructor(public payload: { page: QueryParamsModel }) { }
}

export class VideosPageLoaded implements Action {
    readonly type = VideoActionTypes.VideosPageLoaded;
    constructor(public payload: { results: VideoModel[], totalCount: number, page: QueryParamsModel }) { }
}

export class VideosPageCancelled implements Action {
    readonly type = VideoActionTypes.VideosPageCancelled;
}

export class VideosPageToggleLoading implements Action {
    readonly type = VideoActionTypes.VideosPageToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export class VideosActionToggleLoading implements Action {
    readonly type = VideoActionTypes.VideosActionToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export type VideoActions = VideoOnServerCreated
| VideoCreated
| VideoUpdated
| VideosStatusUpdated
| OneVideoDeleted
| ManyVideosDeleted
| VideosPageRequested
| VideosPageLoaded
| VideosPageCancelled
| VideosPageToggleLoading
| VideosActionToggleLoading;
