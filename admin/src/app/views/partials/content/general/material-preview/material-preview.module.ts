// Angular
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { ClipboardModule } from 'ngx-clipboard';
// Highlight JS
import { HighlightModule } from 'ngx-highlightjs';
// Perfect ScrollBar
import { PerfectScrollbarModule } from 'ngx-perfect-scrollbar';
// Core Module
import { CoreModule } from '../../../../../core/core.module';
import { PortletModule } from '../portlet/portlet.module';
import { MaterialPreviewComponent } from './material-preview.component';

@NgModule({
    imports: [
        CommonModule,
        CoreModule,
        HighlightModule,
        PerfectScrollbarModule,
        PortletModule,
        ClipboardModule,

        // angular material modules
        MatTabsModule,
        MatExpansionModule,
        MatCardModule,
        MatIconModule,
    ],
    exports: [MaterialPreviewComponent],
    declarations: [MaterialPreviewComponent],
})
export class MaterialPreviewModule {
}
