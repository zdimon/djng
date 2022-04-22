import { BaseModel } from '../../../_base/crud';

export class VideoModel extends BaseModel {
    id: number;
    user: number;
    image: string;

    clear() {
        this.id = 0;
        this.image = '';
    }
}
