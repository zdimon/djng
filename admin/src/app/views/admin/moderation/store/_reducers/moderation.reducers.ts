/* -----  --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { ModerationActions, ModerationActionTypes } from '../_actions/moderation.actions';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { ModerationModel } from '../_models/moderation.model';

export interface ModerationsState extends EntityState<ModerationModel> {
    listLoading: boolean;
    actionsloading: boolean;
    totalCount: number;
    lastQuery: QueryParamsModel;
    lastCreatedModerationId: number;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<ModerationModel> = createEntityAdapter<ModerationModel>();

export const initialModerationsState: ModerationsState = adapter.getInitialState({
    listLoading: false,
    actionsloading: false,
    totalCount: 0,
    lastQuery:  new QueryParamsModel({}),
    lastCreatedModerationId: undefined,
    showInitWaitingMessage: true
});

export function moderationReducer(state = initialModerationsState, action: ModerationActions): ModerationsState {
    switch  (action.type) {
        case ModerationActionTypes.ModerationsPageToggleLoading: return {
            ...state, listLoading: action.payload.isLoading, lastCreatedModerationId: undefined
        };
        case ModerationActionTypes.ModerationsActionToggleLoading: return {
            ...state, actionsloading: action.payload.isLoading
        };
        case ModerationActionTypes.ModerationOnServerCreated: return {
            ...state
        };
        case ModerationActionTypes.ModerationCreated: return adapter.addOne(action.payload.moderation, {
             ...state, lastCreatedVideoId: action.payload.moderation.id
        });
        case ModerationActionTypes.ModerationUpdated: return adapter.updateOne(action.payload.partialModeration, state);
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
        case ModerationActionTypes.OneModerationDeleted: return adapter.removeOne(action.payload.id, state);
        case ModerationActionTypes.ManyModerationsDeleted: return adapter.removeMany(action.payload.ids, state);
        case ModerationActionTypes.ModerationsPageCancelled: return {
            ...state, listLoading: false, lastQuery: new QueryParamsModel({})
        };
        case ModerationActionTypes.ModerationsPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initialModerationsState,
                totalCount: action.payload.totalCount,
                listLoading: false,
                lastQuery: action.payload.page,
                showInitWaitingMessage: false
            });
        default: return state;
    }
}

export const getModerationState = createFeatureSelector<ModerationModel>('moderation');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();
