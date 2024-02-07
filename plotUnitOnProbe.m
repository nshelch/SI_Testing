
filename = "C:\Users\somlab\Desktop\NeuropixelSpikeInterface\units.json";
unitStruct = jsondecode(fileread(filename));



numUnits = length(fieldnames(unitStruct));
templateLength = length(unitStruct.unit_0.unit_template(:, 1));
templateCenter = [1:templateLength] - (templateLength / 2);

% Figure plot
hold off
for ii = 0:(numUnits - 1)
    curTemplate = unitStruct.(sprintf('unit_%i', ii)).unit_template;


    templateIdx = 1;
    curTemplate = allTemplates(:, templateIdx);
    xPos = unitStruct.(sprintf('unit_%i', ii)).x_pos;
    yPos = unitStruct.(sprintf('unit_%i', ii)).y_pos;
    plot(templateCenter + xPos, curTemplate + yPos)
    hold on
end