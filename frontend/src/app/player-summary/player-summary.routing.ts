import {ModuleWithProviders} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {PlayerSummaryComponent} from './player-summary.component';


const routes: Routes = [
  { path: '', component: PlayerSummaryComponent, data: { title: 'Player Summary'} },
];

export const routing: ModuleWithProviders<RouterModule> = RouterModule.forChild(routes);