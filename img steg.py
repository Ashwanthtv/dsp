import cv2
import numpy as np

# Load the carrier image
carrier_image = cv2.imread('test.png')
# Load the secret image and resize it to match the dimensions of the carrier image
secret_image = cv2.imread('secret.png')
secret_image = cv2.resize(secret_image, (carrier_image.shape[1], carrier_image.shape[0]))
# Extract the color channels from the carrier and secret images
ra, ga, ba = cv2.split(carrier_image)
rx, gx, bx = cv2.split(secret_image)

# Embed the secret image into the carrier image using LSB steganography
for i in range(carrier_image.shape[0]):
    for j in range(carrier_image.shape[1]):
        nc = ra[i, j] & 254
        ns = rx[i, j] & 128
        ds = ns / 128.0
        fr = nc + ds
        ra[i, j] = np.uint8(fr)

for i in range(carrier_image.shape[0]):
    for j in range(carrier_image.shape[1]):
        nc = ga[i, j] & 254
        ns = gx[i, j] & 128
        ds = ns / 128.0
        fr = nc + ds
        ga[i, j] = np.uint8(fr)

for i in range(carrier_image.shape[0]):
    for j in range(carrier_image.shape[1]):
        nc = ba[i, j] & 254
        ns = bx[i, j] & 128
        ds = ns / 128.0
        fr = nc + ds
        ba[i, j] = np.uint8(fr)

# Create the steganographic image by combining the modified channels
stegmented_image = cv2.merge((ra, ga, ba))

# Extract the LSBs to recover the secret image
recovered_r = np.zeros_like(ra)
recovered_g = np.zeros_like(ga)
recovered_b = np.zeros_like(ba)

for i in range(carrier_image.shape[0]):
    for j in range(carrier_image.shape[1]):
        recovered_r[i, j] = ra[i, j] & 1
        recovered_g[i, j] = ga[i, j] & 1
        recovered_b[i, j] = ba[i, j] & 1

# Scale the recovered bits back to the 0-255 range
recovered_r = (recovered_r * 128).astype(np.uint8)
recovered_g = (recovered_g * 128).astype(np.uint8)
recovered_b = (recovered_b * 128).astype(np.uint8)

# Combine the recovered channels to get the secret image
recovered_image = cv2.merge((recovered_r, recovered_g, recovered_b))

# Display the original carrier, secret, steganographic, and recovered images
cv2.imshow('Carrier Image', carrier_image)
cv2.imshow('Secret Image', secret_image)
cv2.imshow('Steganographic Image', stegmented_image)
cv2.imshow('Recovered Image', recovered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
