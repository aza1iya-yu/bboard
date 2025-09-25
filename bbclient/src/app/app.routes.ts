import { Routes } from '@angular/router';
import { BbList } from './bb-list';
import { BbDetail } from './bb-detail';

export const routes: Routes = [
  { path: ':id', component: BbDetail },
  { path: '', title: '10 последних объявлений', component: BbList }
];
