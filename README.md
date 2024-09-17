
<div align="center">

<p align="center">
  <img src="https://i.imgur.com/B3XGjzQ.png" alt="Deltologic Logo" width="150"/>
</p>

# Amazon SP-API Course

[![Python Version][python_version_img]][python_url]
[![Website][website_img]][company_url]
[![Course][course_img]][course_url]

Welcome to the **Amazon SP-API Course** repository! This repository is part of the Amazon SP-API course available at [courses.deltologic.com][course_url]. It contains examples using the `python-amazon-sp-api` library, which simplifies working with Amazon's SP-API in Python.

</div>

## 🚀 Quick Start

First, clone the repository and prepare your development environment.

### ⚙️ Prepare Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/amazon-sp-api-course/project/directory
```

> **Note:** Running the code from a specific directory (e.g., `FeedsAPI`), add that directory to the `PYTHONPATH` as well. Refer to the `Readme.md` in that directory for details.

### 📄 Prepare `.env` File

Create a `.env` file in the root directory. Copy the contents of `.env.example` and fill in your credentials:

```bash
lwa_app_id=''
lwa_client_secret=''
refresh_token=''

order_id=''
seller_id=''

# Needed for Notifications API:
AWS_SQS_NAME=''
AWS_EVENTBRIDGE_DESTINATION_NAME=''
AWS_SQS_ARN=''
ACCOUNT_ID=''
```

## 📚 What the Repository Offers

We have made an effort to demonstrate the handling of various endpoints on the basis of specific use cases. For example, we use the `searchCatalogItems` operation to calculate the average weight of products that appear as search results for selected keywords.

In **ReportsAPI**, scripts can be run in either 'create report' or 'download report' mode - depending on whether you specify a report identifier or leave it empty. In addition, in the ReportsAPI, you can set the report options to suit your needs (in the <input part>).

In **FeedsAPI**, there are also two modes of running the script available - either to create the feed or to retrieve the result of the feed creation (to check whether the feed was created successfully). The Feeds API itself offers many possibilities, but currently there are two types of feeds available in the repository: 
- `POST_PRODUCT_PRICING_DATA` (to update product prices)
- `POST_INVENTORY_AVAILABILITY_DATA` (to update product inventory)

## 🛠 Django Amazon OAuth App

To run the app, migrate the database and start the server:

```bash
./manage.py migrate
./manage.py runserver
```

## 🌐 Useful Links

- [Amazon SP-API Documentation][amazon_sp_api_url]
- [Deltologic Website][company_url]
- [Course Website][course_url]

## 🎥 Course Preview

Check out a preview of the course on YouTube:

[![Course Preview][youtube_preview_img]][youtube_url]

---

## 🏆 Join Our Community

We invite you to participate in this project! Let's work **together** to create the most **useful** tools for Amazon SP-API developers.

- **Issues:** Have questions or suggestions? Feel free to [open an issue][issues_url].
- **Pull Requests:** Found a bug or have improvements? [Submit a pull request][pulls_url].

Together, we can make this project **better** every day! 😊

## ⭐️ Support Us

If you find this project helpful, please consider:

- Giving us a [star on GitHub][repository_url].
- Sharing the course with your peers.
- Following us on [LinkedIn][linkedin_url].

---

[logo_img]: https://i.imgur.com/B3XGjzQ.png
[company_url]: https://www.deltologic.com/
[course_url]: https://courses.deltologic.com/
[python_version_img]: https://img.shields.io/badge/python-3.x-blue
[python_url]: https://www.python.org/
[license_img]: https://img.shields.io/badge/license-MIT-green
[license_url]: LICENSE
[website_img]: https://img.shields.io/badge/website-Deltologic-blue
[course_img]: https://img.shields.io/badge/course-Amazon%20SP--API%20Course-orange
[amazon_sp_api_url]: https://developer-docs.amazon.com/sp-api/
[youtube_preview_img]: https://img.youtube.com/vi/zpUsBHuH0G8/0.jpg
[youtube_url]: https://youtu.be/zpUsBHuH0G8
[issues_url]: https://github.com/Deltologic/amazon-sp-api-course/issues
[pulls_url]: https://github.com/Deltologic/amazon-sp-api-course/pulls
[repository_url]: https://github.com/Deltologic/amazon-sp-api-course
[linkedin_url]: https://www.linkedin.com/company/deltologic-software/