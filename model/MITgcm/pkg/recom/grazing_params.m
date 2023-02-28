pzdia = 0.5;
sdiasq = 0.02;
epsilon = 0.01;

nx = 101;
ny = 71;
dmax = 0.7;
for i=1:nx,
  dian(i) = (i-1)*dmax/(nx-1);
  diansq = dian(i)*dian(i);
  varpzdia = pzdia * diansq / (sdiasq + diansq);  
  fdiaN1 = varpzdia*dian(i);
  fdiaN2 = pzdia*dian(i);
  for j=1:ny,
    phyn(j) = (j-1)*dmax/(ny-1);
    food1 = phyn(j) +fdiaN1;
    food2 = phyn(j) +fdiaN2;
  
    foodsq1 = food1*food1;
    grazingFlux1(i,j) = foodsq1 / (epsilon+foodsq1);
    grazingFlux_phy1(i,j) = grazingFlux1(i,j) * phyn(j)/food1;
    grazingFlux_dia1(i,j) = grazingFlux1(i,j) * fdiaN1/food1;
  
    foodsq2 = food2*food2;
    grazingFlux2(i,j) = foodsq2 / (epsilon+foodsq2);
    grazingFlux_phy2(i,j) = grazingFlux2(i,j) * phyn(j)/food2;
    grazingFlux_dia2(i,j) = grazingFlux2(i,j) * fdiaN2/food2;
  end
end

%make plots
figure(1);

subplot(2,2,1)
v = (0:0.05:1);
[hh,cc] = contourf(dian,phyn,grazingFlux1',v);
caxis([0 1]);
set(gca,'PlotBoxAspectRatio',[1 1 1],'FontSize',12);
title('variable preference');
subplot(2,2,2)
v = (0:0.05:1);
[hh,cc] = contourf(dian,phyn,grazingFlux2',v);
caxis([0 1]);
set(gca,'PlotBoxAspectRatio',[1 1 1],'FontSize',12);
title('constant preference');
subplot(2,2,3)
v = (-0.2:0.02:0.2);
[hh,cc] = contourf(dian,phyn,grazingFlux1' - grazingFlux2',v);
caxis([-1 1]);
set(gca,'PlotBoxAspectRatio',[1 1 1],'FontSize',12);
title('difference');
colorbar

figure(2);

subplot(2,2,1)
v = (0:0.05:1);
[hh,cc] = contourf(dian,phyn,grazingFlux_dia1',v);
caxis([0 1]);
set(gca,'PlotBoxAspectRatio',[1 1 1],'FontSize',12);
title('variable preference');
subplot(2,2,2)
v = (0:0.05:1);
[hh,cc] = contourf(dian,phyn,grazingFlux_dia2',v);
caxis([0 1]);
set(gca,'PlotBoxAspectRatio',[1 1 1],'FontSize',12);
title('constant preference');
subplot(2,2,3)
v = (-0.2:0.02:0.2);
[hh,cc] = contourf(dian,phyn,grazingFlux_dia1' - grazingFlux_dia2',v);
caxis([-1 1]);
set(gca,'PlotBoxAspectRatio',[1 1 1],'FontSize',12);
title('difference');
colorbar

