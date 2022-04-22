
// NGRX
import { createEntityAdapter, EntityAdapter, EntityState, Update } from '@ngrx/entity';
import { createFeatureSelector } from '@ngrx/store';
// CRUD
import { QueryParamsModel } from '../../../_base/crud';
// Actions
import { VideoActions, VideoActionTypes } from '../_actions/video.actions';
// Models
import { VideoModel } from '../_models/video.model';

export interface VideosState extends EntityState<VideoModel> {
    listLoading: boolean;
    actionsloading: boolean;
    totalCount: number;
    lastQuery: QueryParamsModel;
    lastCreatedVideoId: number;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<VideoModel> = createEntityAdapter<VideoModel>();

export const initialVideosState: VideosState = adapter.getInitialState({
    listLoading: false,
    actionsloading: false,
    totalCount: 0,
    lastQuery:  new QueryParamsModel({}),
    lastCreatedVideoId: undefined,
    showInitWaitingMessage: true,
});

export function videosReducer(state = initialVideosState, action: VideoActions): VideosState {
    switch  (action.type) {
        case VideoActionTypes.VideosPageToggleLoading: return {
            ...state, listLoading: action.payload.isLoading, lastCreatedVideoId: undefined,
        };
        case VideoActionTypes.VideosActionToggleLoading: return {
            ...state, actionsloading: action.payload.isLoading,
        };
        case VideoActionTypes.VideoOnServerCreated: return {
            ...state,
        };
        case VideoActionTypes.VideoCreated: return adapter.addOne(action.payload.video, {
             ...state, lastCreatedVideoId: action.payload.video.id,
        });
        case VideoActionTypes.VideoUpdated: return adapter.updateOne(action.payload.partialProduct, state);
        // case VideoActionTypes.VideosStatusUpdated: {
        //     const _partialVideos: Update<VideoModel>[] = [];
        //     for (let i = 0; i < action.payload.videos.length; i++) {
        //         _partialVideos.push({
        //             id: action.payload.results[i].id,
        //             changes: {
        //                status: action.payload.status
        //             }
        //         });
        //     }
        //     return adapter.updateMany(_partialVideos, state);
        // }
        case VideoActionTypes.OneVideoDeleted: return adapter.removeOne(action.payload.id, state);
        case VideoActionTypes.ManyVideosDeleted: return adapter.removeMany(action.payload.ids, state);
        case VideoActionTypes.VideosPageCancelled: return {
            ...state, listLoading: false, lastQuery: new QueryParamsModel({}),
        };
        case VideoActionTypes.VideosPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initialVideosState,
                totalCount: action.payload.totalCount,
                listLoading: false,
                lastQuery: action.payload.page,
                showInitWaitingMessage: false,
            });
        default: return state;
    }
}

export const getVideoState = createFeatureSelector<VideoModel>('videos');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal,
} = adapter.getSelectors();
