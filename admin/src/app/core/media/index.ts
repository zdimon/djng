// Context
// export { ECommerceDataContext } from './_server/_e-commerce.data-context';

// Models and Consts
export { VideoModel } from './video/_models/video.model';

// DataSources
export { VideosDataSource } from './video/_data-sources/video.datasource';

// Actions
// Customer Actions =>

// Video actions =>
export {
    VideoActionTypes,
    VideoActions,
    VideoOnServerCreated,
    VideoCreated,
    VideoUpdated,
    VideosStatusUpdated,
    OneVideoDeleted,
    ManyVideosDeleted,
    VideosPageRequested,
    VideosPageLoaded,
    VideosPageCancelled,
    VideosPageToggleLoading,
    VideosActionToggleLoading,
} from './video/_actions/video.actions';

// Effects

export { VideoEffects } from './video/_effects/video.effects';

// Reducers
export { videosReducer } from './video/_reducers/video.reducers';

// Product selectors
export {
    selectVideoById,
    selectVideosInStore,
    selectVideosPageLoading,
    selectVideosPageLastQuery,
    selectLastCreatedVideoId,
    selectHasVideosInStore,
    selectVideosActionLoading,
    selectVideosInitWaitingMessage,
} from './video/_selectors/video.selectors';

// Services

export { VideoService } from './video/_services/';
