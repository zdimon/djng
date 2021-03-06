/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { UserActions, UserActionTypes } from '../_actions/user.actions';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { UserModel } from '../_models/user.model';

export interface UsersState extends EntityState<UserModel> {
    listLoading: boolean;
    actionsloading: boolean;
    totalCount: number;
    lastQuery: QueryParamsModel;
    lastCreatedUserId: number;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<UserModel> = createEntityAdapter<UserModel>();

export const initialUsersState: UsersState = adapter.getInitialState({
    listLoading: false,
    actionsloading: false,
    totalCount: 0,
    lastQuery:  new QueryParamsModel({}),
    lastCreatedUserId: undefined,
    showInitWaitingMessage: true
});

export function userReducer(state = initialUsersState, action: UserActions): UsersState {
    switch  (action.type) {
        case UserActionTypes.UsersPageToggleLoading: return {
            ...state, listLoading: action.payload.isLoading, lastCreatedUserId: undefined
        };
        case UserActionTypes.UsersActionToggleLoading: return {
            ...state, actionsloading: action.payload.isLoading
        };
        case UserActionTypes.UserOnServerCreated: return {
            ...state
        };
        case UserActionTypes.UserCreated: return adapter.addOne(action.payload.user, {
             ...state, lastCreatedVideoId: action.payload.user.id
        });
        case UserActionTypes.UserUpdated: return adapter.updateOne(action.payload.partialUser, state);
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
        case UserActionTypes.OneUserDeleted: return adapter.removeOne(action.payload.id, state);
        case UserActionTypes.ManyUsersDeleted: return adapter.removeMany(action.payload.ids, state);
        case UserActionTypes.UsersPageCancelled: return {
            ...state, listLoading: false, lastQuery: new QueryParamsModel({})
        };
        case UserActionTypes.UsersPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initialUsersState,
                totalCount: action.payload.totalCount,
                listLoading: false,
                lastQuery: action.payload.page,
                showInitWaitingMessage: false
            });
        default: return state;
    }
}

export const getUserState = createFeatureSelector<UserModel>('user');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();
