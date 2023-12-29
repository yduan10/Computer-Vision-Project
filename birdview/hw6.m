
video = VideoReader('birdview/birdview.mp4');
numFrames = video.NumberOfFrames;

frames(1: numFrames) = struct('cdata', zeros(video.Height, video.Width, 3, 'uint8'), 'colormap', []);
binary = zeros(video.Height, video.Width, numFrames - 1); 
mhi = zeros(video.Height, video.Width, numFrames - 1); 
f = fspecial('gaussian', [4 4], 10); 

for k = 1: numFrames

frames(k).cdata = imfilter(rgb2gray(read(video, k)), f, 'replicate');
end

t = 0.25;
for i = 2:numFrames
diff = frames(i).cdata - frames(i - 1).cdata;
binary(:,:, i - 1) = (im2bw(diff, t)); 
mhi(:,:, i) = 60 * binary(:,:, i - 1);

for j = 1:video.height
for k = 1:video.width
if (mhi(j, k, i) == 0)
    mhi(j, k, i) = max(0, mhi(j, k, i - 1) - 2); 
end
end

end

end

implay(mhi)


%func
function mu = generateMu(x_i, y_j, x_bar, y_bar, boxIm1)
    height = size(boxIm1,1);
    width = size(boxIm1,2);
    mu = 0;
    for i = 1:height
        for j = 1:width
            mu = mu + (j - x_bar)^x_i *(i - y_bar)^y_j *boxIm1(i, j);
        end
    end
end
function Nvals = similitudeMoments(boxIm1)
    height = size(boxIm1,1);
    width = size(boxIm1,2);
    m10 = 0;
    m01 = 0;
    m00 = 0;
    for i = 1:height
        for j = 1:width
            m10 = m10 + j*boxIm1(i, j);
            m01 = m01 + i*boxIm1(i, j);
            m00 = m00 + boxIm1(i, j);
        end
    end
    x_bar = m10/m00;
    y_bar = m01/m00;
    mu02 = generateMu(0, 2, x_bar, y_bar, boxIm1);
    eta02 = mu02/m00^(2/2 +1);
    mu03 = generateMu(0, 3, x_bar, y_bar, boxIm1);
    eta03 = mu03/m00^(3/2 +1);
    mu11 = generateMu(1, 1, x_bar, y_bar, boxIm1);
    eta11 = mu11/m00^(2/2 +1);
    mu12 = generateMu(1, 2, x_bar, y_bar, boxIm1);
    eta12 = mu12/m00^(3/2 +1);
    mu20 = generateMu(2, 0, x_bar, y_bar, boxIm1);
    eta20 = mu20/m00^(2/2 +1);
    mu21 = generateMu(2, 1, x_bar, y_bar, boxIm1);
    eta21 = mu21/m00^(3/2 +1);
    mu30 = generateMu(3, 0, x_bar, y_bar, boxIm1);
    eta30 = mu30/m00^(3/2 +1);
    Nvals = [eta02, eta03, eta11, eta12, eta20, eta21, eta30];
end
