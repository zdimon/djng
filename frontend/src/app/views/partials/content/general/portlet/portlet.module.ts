// Angular
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { MatProgressBarModule, MatProgressSpinnerModule } from '@angular/material';

// Module
import { CoreModule } from '../../../../../core/core.module';
import { PortletBodyComponent } from './portlet-body.component';
import { PortletFooterComponent } from './portlet-footer.component';
import { PortletHeaderComponent } from './portlet-header.component';
// Portlet
import { PortletComponent } from './portlet.component';

@NgModule({
    imports: [
        CommonModule,
        CoreModule,
        MatProgressSpinnerModule,
        MatProgressBarModule,
    ],
    declarations: [
        PortletComponent,
        PortletHeaderComponent,
        PortletBodyComponent,
        PortletFooterComponent,
    ],
    exports: [
        PortletComponent,
        PortletHeaderComponent,
        PortletBodyComponent,
        PortletFooterComponent,
    ],
})
export class PortletModule {
}
