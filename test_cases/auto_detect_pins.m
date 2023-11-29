    % Define the replacement mappings
replaceMap = {'SL', 'SS', 'ES', 'L', 'M', 'S'};
replaceWithMap = {'sehrleicht', 'sehrschwer', 'extremschwer', 'leicht', 'mittel', 'schwer'};
keys = {'schwierigkeit', 'pins', 'kanten'};

% Location of images files


% Grid axes
x = [0.0227; 0.1404; 0.2565; 0.3735; 0.4888; 0.6041; 0.7186; 0.8356; 0.9509; 1.0670; 1.1807] * 1e3;
y = [0.0268; 0.1808; 0.3366; 0.4925; 0.6447; 0.8005; 0.9563; 1.1104; 1.2662; 1.4238; 1.5797] * 1e3;
[X, Y] = meshgrid(x, y);

% Measure redness
roi_size = 30;

% Initialize an array to store the counts
blue_pixel_counts = zeros(11, 11);

% List all files
files = dir("C:\Users\P008883\Dropbox\txt\board_game\filtered\*.jpeg");

for i = 1:length(files)
    file = files(i);
    fname_components = strsplit(file.name, '_');
    n_pins = str2double(fname_components{2});
    name = strsplit(file.name, '.');
    path = fullfile(file.folder, file.name);
    importboard(path);
    eval(strcat('img = ', name{1}, ';'));
    % Rotate if needed
    if size(img, 1) == 1200
        img = imrotate(img, 90);
    end
    % Loop through each point and measure the red pixels in the specified radius
    for u = 1:11
        for v = 1:11
            x = X(u, v);
            y = Y(u, v);

            % Create a circular mask
            [X_mask, Y_mask] = meshgrid(1:roi_size, 1:roi_size);
            mask = ((X_mask - (roi_size+1)/2).^2 + (Y_mask - (roi_size+1)/2).^2) <= (roi_size/2)^2;

            % Extract the blue channel within the circular ROI
            roi_blue_channel = img(int32(y - roi_size/2):int32(y + roi_size/2), int32(x - roi_size/2):int32(x + roi_size/2), 3);
            roi_blue_values = roi_blue_channel(mask);

            blue_pixel_counts(u, v) = mean(roi_blue_values);
        end
    end

    sorted_pixels = sort(blue_pixel_counts(:));
    threshold = sorted_pixels(n_pins);
    % Plot the original image with overlay
    figure;
    imagesc(img);
    colormap('gray');
    hold on;
    
    % Create a better name
    verbose_name = name{1};
    for i = 1:length(replaceMap)
        verbose_name = strrep(verbose_name, replaceMap{i}, replaceWithMap{i});
    end

    splitName = strsplit(verbose_name, '_');
    version = '';
    if length(splitName) > length(keys)
        version = strcat('_version-', splitName{end});
        splitName = splitName(1:numel(keys));
    end
    combinedCellArray = strcat(keys, '-', splitName);
    full_name = strcat(strjoin(combinedCellArray, '_'), version);
    
    % Loop through the mappings and replace substrings
    disp(['tests.update({"', full_name, '" : ['])
    for u = 1:11
        for v = 1:11
            if blue_pixel_counts(u, v) <= threshold
                plot(X(u, v), Y(u, v), 'ro', 'MarkerSize', 10);
                disp(['(', num2str(u), ', ', num2str(v), '),'])
            end
        end
    end
    disp(']})')
    hold off;
    title(full_name, 'Interpreter', 'none');
    axis('off');
    saveas(gcf, fullfile('detected', strcat(full_name, '.png')));
    close
end




