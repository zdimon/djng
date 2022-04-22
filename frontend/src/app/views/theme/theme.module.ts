import { CommonModule } from '@angular/common';
// Angular
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
// Angular Material
import { MatButtonModule, MatProgressBarModule, MatTabsModule, MatTooltipModule } from '@angular/material';
import { RouterModule } from '@angular/router';
// NgBootstrap
import { NgbProgressbarModule, NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';
import { EffectsModule } from '@ngrx/effects';
// NGRX
import { StoreModule } from '@ngrx/store';
// Loading bar
import { LoadingBarModule } from '@ngx-loading-bar/core';
// Translation
import { TranslateModule } from '@ngx-translate/core';
// SVG inline
import { InlineSVGModule } from 'ng-inline-svg';
// Ngx DatePicker
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';
// Perfect Scrollbar
import { PerfectScrollbarModule } from 'ngx-perfect-scrollbar';
import { NgxPermissionsModule } from 'ngx-permissions';
import { PermissionEffects, permissionsReducer, RoleEffects, rolesReducer } from '../../core/auth';
// Core Module
import { CoreModule } from '../../core/core.module';
import { PagesModule } from '../pages/pages.module';
import { PartialsModule } from '../partials/partials.module';
import { AsideLeftComponent } from './aside/aside-left.component';
import { BaseComponent } from './base/base.component';
import { BrandComponent } from './brand/brand.component';
import { ErrorPageComponent } from './content/error-page/error-page.component';
import { FooterComponent } from './footer/footer.component';
import { HeaderMobileComponent } from './header/header-mobile/header-mobile.component';
import { HeaderComponent } from './header/header.component';
import { MenuHorizontalComponent } from './header/menu-horizontal/menu-horizontal.component';
import { TopbarComponent } from './header/topbar/topbar.component';
import { HtmlClassService } from './html-class.service';

@NgModule({
    declarations: [
        BaseComponent,
        FooterComponent,

        // headers
        HeaderComponent,
        BrandComponent,
        HeaderMobileComponent,

        // subheader
        // SubheaderComponent,

        // topbar components
        TopbarComponent,

        // aside left menu components
        AsideLeftComponent,

        // horizontal menu components
        MenuHorizontalComponent,

        ErrorPageComponent,
    ],
    exports: [
        BaseComponent,
        FooterComponent,

        // headers
        HeaderComponent,
        BrandComponent,
        HeaderMobileComponent,

        // subheader
        // SubheaderComponent,

        // topbar components
        TopbarComponent,

        // aside left menu components
        AsideLeftComponent,

        // horizontal menu components
        MenuHorizontalComponent,

        ErrorPageComponent,
    ],
    providers: [
        HtmlClassService,
    ],
    imports: [
        CommonModule,
        RouterModule,
        NgxPermissionsModule.forChild(),
        StoreModule.forFeature('roles', rolesReducer),
        StoreModule.forFeature('permissions', permissionsReducer),
        EffectsModule.forFeature([PermissionEffects, RoleEffects]),
        PagesModule,
        PartialsModule,
        CoreModule,
        PerfectScrollbarModule,
        FormsModule,
        MatProgressBarModule,
        MatTabsModule,
        MatButtonModule,
        MatTooltipModule,
        TranslateModule.forChild(),
        LoadingBarModule,
        NgxDaterangepickerMd,
        InlineSVGModule,

        // ng-bootstrap modules
        NgbProgressbarModule,
        NgbTooltipModule,
    ],
})
export class ThemeModule {
}
